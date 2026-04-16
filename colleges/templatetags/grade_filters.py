from django import template

register = template.Library()

@register.filter
def grade_badge_class(grade):
    if not grade:
        return 'bg-secondary'
    
    grade_mapping = {
        'A+': 'bg-success',
        'A': 'bg-primary',
        'B+': 'bg-info',
        'B': 'bg-warning text-dark',
        'C': 'bg-secondary',
        'D': 'bg-danger',
        'F': 'bg-dark',
    }
    
    return grade_mapping.get(grade, 'bg-secondary')
