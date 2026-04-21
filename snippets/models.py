from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Create your models here.
"""
These lines are setting up the "dropdown menus" for your model. 
In Django, if you want a field to have a specific list of options,
you provide a list of tuples.
"""
LEXERS=[item for item in get_all_lexers() if item[1]]
"""
It calls get_all_lexers() from the Pygments library.
This function returns a massive list of every programming language 
it knows how to highlight (Python, Java, C++, etc.).
The if item[1] part ensures we only keep languages 
that actually have "aliases" (short names like py for Python).
"""
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
"""
It creates a list of pairs: (stored_value, display_name).
item[1][0] is the short code (e.g., "python"). This is what gets saved in the database.
item[0] is the pretty name (e.g., "Python"). This is what a user sees in a form.
"""
STYLE_CHOICES = sorted([(item,item) for item in get_all_styles()])
"""
Similar to above, but for color themes (like "Monokai", "Friendly", or "Dark").
It gets all available themes from Pygments and turns them into a list of choices.
"""
class Snippet(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=100, blank=True, default="")
    code=models.TextField()
    linenos=models.BooleanField(default=False)
    language=models.CharField(choices=LANGUAGE_CHOICES, default="python", max_length=100)
    style=models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)

    class Meta:
        ordering=["created"]



