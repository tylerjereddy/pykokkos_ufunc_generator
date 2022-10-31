import template

def main(ufunc_mod_path: str):
    # automatically write out some ufunc workunits + exposed
    # functions for pykokkos, to reduce the copy-paste burden
    with open(ufunc_mod_path, 'w') as ufunc_module:
        for ufunc_name in ["cosh", "tanh", "trunc", "round"]:
            ufunc_module.write(template.template_str.format(ufunc_name=ufunc_name))






if __name__ == "__main__":
    main("ufuncs_auto.py")
