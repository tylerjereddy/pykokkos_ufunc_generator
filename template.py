template_str_workunit = '''
@pk.workunit
def {ufunc_name}_impl_1d_{view_type}(tid: int, view: pk.View1D[pk.{view_type}], out: pk.View1D[pk.{view_type}]):
    out[tid] = {ufunc_name}(view[tid])


@pk.workunit
def {ufunc_name}_impl_2d_{view_type}(tid: int, view: pk.View2D[pk.{view_type}], out: pk.View2D[pk.{view_type}]):
    for i in range(view.extent(1)):
        out[tid][i] = {ufunc_name}(view[tid][i])


@pk.workunit
def {ufunc_name}_impl_3d_{view_type}(tid: int, view: pk.View3D[pk.{view_type}], out: pk.View3D[pk.{view_type}]):
    for i in range(view.extent(1)):
        for j in range(view.extent(2)):
            out[tid][i][j] = {ufunc_name}(view[tid][i][j])
'''


template_str_main_func_top = '''
def {ufunc_name}(view):
    if "int" in str(view.dtype):
        # special case defined in API std
        return view
    out = pk.View(view.shape, dtype=view.dtype)
    if len(view.shape) > 3:
        raise NotImplementedError("only up to 3D views currently supported for {ufunc_name}() ufunc.")
        '''

template_str_main_func_mid = '''
    {cond} "{view_type}" in str(view.dtype):
        if view.shape == ():
            pk.parallel_for(1, {ufunc_name}_impl_1d_{view_type_2}, view=view, out=out)
        elif len(view.shape) == 1:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_1d_{view_type_2}, view=view, out=out)
        elif len(view.shape) == 2:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_2d_{view_type_2}, view=view, out=out)
        elif len(view.shape) == 3:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_3d_{view_type_2}, view=view, out=out)
'''

template_str_main_func_bottom = '''
    else:
        raise NotImplementedError
    return out
'''
