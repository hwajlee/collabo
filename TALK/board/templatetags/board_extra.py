from django import template
register = template.Library()
@register.simple_tag
def art_voted(article, user):
    return article.is_voted(user)

@register.simple_tag
def rep_voted(reply, user):
    return reply.is_voted(user)