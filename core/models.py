from django.db import models

# Create your models here.

from django.contrib.auth.models import User
import re

class Directory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    availability_changed_at = models.DateTimeField(auto_now=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    parent_directory = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

class File(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    availability_changed_at = models.DateTimeField(auto_now=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    compiled_content = models.TextField(blank=True)

    def divide_into_sections(self):
    # regular expressions for different section types
        type_regex = {
            'comment': r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)',
            'compiler_directives': r'^#.*',
            'variable_declarations': r'^(int|char|float|double|long)\s+\w+(\s*[=,;].*)?',
            'assembly_insert': r'__asm__\([\s\S]*?\)',
        }

        lines = self.content.split('\n')

        section_lines = []
        section_type = 'procedure'
        
        line_counter = 1
        start_line = 1

        for line in lines:
            for section, regex in type_regex.items():
                if re.match(regex, line.strip()):
                    if section_lines and section_type:
                        self.save_section(section_lines, section_type, start_line, line_counter - 1)
                        section_lines = []
                    section_type = section
                    start_line = line_counter
                    break
            else:
                section_type = 'procedure'
            section_lines.append(line)
            line_counter += 1

        if section_lines and section_type:
            self.save_section(section_lines, section_type, start_line, line_counter - 1)

        self.save()

    def save_section(self, section_lines, section_type, start_line, end_line):
        content = '\n'.join(section_lines)
        FileSection.objects.create(
        file=self,
        name='Some Name',
        description='Some Description',
        section_start=start_line,
        section_end=end_line,
        section_type=SectionType.objects.get(type=section_type),
        section_status=SectionStatus.objects.get(id=1),
        status_data=StatusData.objects.get(id=1),
        content=content
    )




class CompilationOption(models.Model):
    STANDARD_CHOICES = [('c89', 'C89'), ('c99', 'C99'), ('c11', 'C11')]
    OPTIMIZATION_CHOICES = [('nogcse', 'nogcse'), ('noinvariant', 'noinvariant'), ('noinduction', 'noinduction')]
    PROCESSOR_CHOICES = [('mcs51', 'MCS51'), ('z80', 'Z80'), ('stm8', 'STM8')]

    standard = models.CharField(max_length=10, choices=STANDARD_CHOICES, default='C89')
    optimization = models.CharField(max_length=12, choices=OPTIMIZATION_CHOICES, default='nogcse')
    processor = models.CharField(max_length=10, choices=PROCESSOR_CHOICES, default='MCS51')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class SectionType(models.Model):
    TYPE_CHOICES = [
        ('procedure', 'Procedure'),
        ('comment', 'Comment'),
        ('compiler_directives', 'Compiler Directives'),
        ('variable_declarations', 'Variable Declarations'),
        ('assembly_insert', 'Assembly Insert')
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

class SectionStatus(models.Model):
    STATUS_CHOICES = [
        ('compiles_with_warnings', 'Compiles with warnings'),
        ('compiles_without_warnings', 'Compiles without warnings'),
        ('does_not_compile', 'Does not compile')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

class StatusData(models.Model):
    DATA_CHOICES = [
        ('compilation_error', 'Compilation error'),
        ('line_number_with_warning', 'Line number with warning')
    ]
    data = models.CharField(max_length=50, choices=DATA_CHOICES)

class FileSection(models.Model):
    main_section = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    section_start = models.IntegerField()
    section_end = models.IntegerField()
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    section_status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
    status_data = models.ForeignKey(StatusData, on_delete=models.CASCADE)
    content = models.TextField()
