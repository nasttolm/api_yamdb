from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    pass
