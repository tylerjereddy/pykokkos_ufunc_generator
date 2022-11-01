import template

def main(ufunc_mod_path: str):
    # automatically write out some ufunc workunits + exposed
    # functions for pykokkos, to reduce the copy-paste burden
    with open(ufunc_mod_path, 'w') as ufunc_module:
        for ufunc_name in ["trunc"]:
            for view_type in ["double",
                              "float",
                              "int8",
                              "int16",
                              "int32",
                              "int64",
                              "uint8",
                              "uint16",
                              "uint32",
                              "uint64"]:
                ufunc_module.write(template.template_str_workunit.format(ufunc_name=ufunc_name,
                                                                     view_type=view_type))
            ufunc_module.write(template.template_str_main_func_top.format(ufunc_name=ufunc_name,
                                                                 view_type=view_type))
            for view_type in ["double",
                              "float",
                              "uint8",
                              "uint16",
                              "uint32",
                              "uint64",
                              "int8",
                              "int16",
                              "int32",
                              "int64"]:
                if view_type == "double":
                    cond = "if"
                else:
                    cond = "elif"
                ufunc_module.write(template.template_str_main_func_mid.format(ufunc_name=ufunc_name,
                                                                     view_type=view_type,
                                                                     cond=cond))

            ufunc_module.write(template.template_str_main_func_bottom.format(ufunc_name=ufunc_name,
                                                                 view_type=view_type))






if __name__ == "__main__":
    main("ufuncs_auto.py")
