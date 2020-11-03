from rest_framework.permissions import BasePermission  

class IsFuncionarioUser(BasePermission):
    """
    Allows access only to Funcionario users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_funcionario)


class IsEmpresaUser(BasePermission):
    """
    Allows access only to Empresa users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_empresa)
