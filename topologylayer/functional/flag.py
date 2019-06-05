from __future__ import print_function

from torch.autograd import Variable, Function
from .cohom_cpp import SimplicialComplex, persistenceForward, persistenceBackwardFlag, persistenceForwardHom

class FlagDiagram(Function):
    """
    Compute Flag complex persistence using point coordinates

    forward inputs:
        X - simplicial complex
        y - N x D torch.float tensor of coordinates
        maxdim - maximum homology dimension
        alg - algorithm
            'hom' = homology (default)
            'cohom' = cohomology
    """
    @staticmethod
    def forward(ctx, X, y, maxdim, alg='hom'):
        X.extendFlag(y)
        if alg == 'hom':
            ret = persistenceForwardHom(X, maxdim)
        elif alg == 'cohom':
            ret = persistenceForward(X, maxdim)
        ctx.X = X
        ctx.save_for_backward(y)
        return tuple(ret)

    @staticmethod
    def backward(ctx, *grad_dgms):
        # print(grad_dgms)
        X = ctx.X
        y, = ctx.saved_tensors
        grad_ret = list(grad_dgms)
        grad_y = persistenceBackwardFlag(X, y, grad_ret)
        return None, grad_y, None, None
