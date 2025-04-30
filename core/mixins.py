from django.contrib.auth.mixins import UserPassesTestMixin

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []
    
    def test_func(self):
        return self.request.user.role in self.allowed_roles