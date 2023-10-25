class TitleMixin:
    title: str = None

    def get_context_data(self, **kwargs: dict[str, any]) -> dict[str, any]:
        context: dict = super().get_context_data(**kwargs)
        context['title']: str = self.title

        return context
