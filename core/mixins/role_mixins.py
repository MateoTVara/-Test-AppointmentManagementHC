from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# Specific role mixins
class DoctorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['DOCTOR']

class ManagementRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['MANAGEMENT', 'ADMIN']

class AttendantRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ATTENDANT', 'MANAGEMENT', 'ADMIN']