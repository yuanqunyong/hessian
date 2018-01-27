# pylint: disable=E1101, C0103, C0111
'''
Computes the Hessian
'''
import torch


def hessian(output, parameters):
    '''
    Compute the Hessian of `output` with respect to `parameters`
    '''
    if parameters[0].is_cuda:
        Tensor = torch.cuda.FloatTensor
    else:
        Tensor = torch.FloatTensor

    n = sum(p.numel() for p in parameters)
    hess = Tensor(n, n).fill_(0)

    ai = 0
    for i, param in enumerate(parameters):
        grad = torch.autograd.grad(output, param, create_graph=True)
        grad = grad[0].contiguous().view(-1)

        for j in range(param.numel()):
            row = torch.autograd.grad(grad[j], parameters[i:], retain_graph=True)
            row = torch.cat([x.data.contiguous().view(-1) for x in row])[j:]

            hess[ai, ai:] += row
            if ai + 1 < n:
                hess[ai + 1:, ai] += row[1:]
            del row
            ai += 1
        del grad

    return hess
