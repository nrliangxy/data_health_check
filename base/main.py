from methods.gits import is_empty

class BaseHealthCheck(object):
    # 独立且必须有的字段
    MUST_REQUIRE_FIELD_SET = set()
    # 联合判断的字段,必须包含其中一个[(f1, f2, f3), (f4, f5)]
    REQUIRE_ONE_FIELD_GROUPS = []
    
    @classmethod
    def required(cls, data=None):
        """验证data是否None"""
        return True if data else False
    
    @classmethod
    def required_one(cls, *args):
        """验证多个data是否存在一个不为None"""
        return any(cls.required(arg) for arg in args)
    
    @classmethod
    def validate(cls, data: dict) -> (bool, str):
        required_validated=set()
        validate_funcs = {
            k : getattr(cls, k) for k in dir(cls) if k.startswith("valid_") and getattr(cls, k, None)
        }
        for field_group in cls.REQUIRE_ONE_FIELD_GROUPS:
            fields = [data.get(i, None) for i in field_group]
            if not cls.required_one(*fields):
                return False, "all field %s is missing" % str(field_group)
        for field in data.keys():
            if field in cls.MUST_REQUIRE_FIELD_SET:
                if is_empty(data[field]):
                    return False, "%s is empty" % field
                required_validated.add(field)
            valid_func_name = 'valid_{}'.format(field)
            func = validate_funcs.pop(valid_func_name, None)
            if not func:
                continue
            result = func(**data)
            if result:
                continue
            else:
                return False, "%s error" % field
        if len(required_validated) != len(cls.MUST_REQUIRE_FIELD_SET):
            return False, "fields %s is not valid" % (cls.MUST_REQUIRE_FIELD_SET - required_validated)
        return True, "success"
    