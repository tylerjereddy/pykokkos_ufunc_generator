template_str = '''
@pk.workunit
def {ufunc_name}_impl_1d_double(tid: int, view: pk.View1D[pk.double], out: pk.View1D[pk.double]):
    out[tid] = {ufunc_name}(view[tid])


@pk.workunit
def {ufunc_name}_impl_2d_double(tid: int, view: pk.View2D[pk.double], out: pk.View2D[pk.double]):
    for i in range(view.extent(1)):
        out[tid][i] = {ufunc_name}(view[tid][i])


@pk.workunit
def {ufunc_name}_impl_1d_float(tid: int, view: pk.View1D[pk.float], out: pk.View1D[pk.float]):
    out[tid] = {ufunc_name}(view[tid])


@pk.workunit
def {ufunc_name}_impl_2d_float(tid: int, view: pk.View2D[pk.float], out: pk.View2D[pk.float]):
    for i in range(view.extent(1)):
        out[tid][i] = {ufunc_name}(view[tid][i])


def {ufunc_name}(view):
    """

    Parameters
    ----------
    view : pykokkos view
           Input view.

    Returns
    -------
    out : pykokkos view
           Output view.

    """
    if len(view.shape) > 2:
        raise NotImplementedError("only up to 2D views currently supported for {ufunc_name}() ufunc.")
    if "double" in str(view.dtype) or "float64" in str(view.dtype):
        out = pk.View([*view.shape], dtype=pk.float64)
        if len(view.shape) == 1:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_1d_double, view=view, out=out)
        elif len(view.shape) == 2:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_2d_double, view=view, out=out)
    elif "float" in str(view.dtype):
        out = pk.View([*view.shape], dtype=pk.float32)
        if len(view.shape) == 1:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_1d_float, view=view, out=out)
        elif len(view.shape) == 2:
            pk.parallel_for(view.shape[0], {ufunc_name}_impl_2d_float, view=view, out=out)
    else:
        raise NotImplementedError
    return out

'''
