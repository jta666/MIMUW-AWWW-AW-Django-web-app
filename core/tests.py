from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Directory, File, CompilationOption, SectionType, SectionStatus, StatusData, FileSection

class DirectoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(
            name="Test Directory",
            owner=self.user,
            description="Test Description"
        )
    
    def test_directory_creation(self):
        self.assertIsInstance(self.directory, Directory)
        self.assertEqual(self.directory.name, "Test Directory")
        self.assertEqual(self.directory.description, "Test Description")
        self.assertEqual(self.directory.owner, self.user)
        self.assertTrue(self.directory.is_available)


class FileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(
            name="Test Directory",
            owner=self.user,
            description="Test Description"
        )
        self.file = File.objects.create(
            name="Test File",
            owner=self.user,
            directory=self.directory,
            content="Test Content"
        )
    
    def test_file_creation(self):
        self.assertIsInstance(self.file, File)
        self.assertEqual(self.file.name, "Test File")
        self.assertEqual(self.file.content, "Test Content")
        self.assertEqual(self.file.directory, self.directory)
        self.assertEqual(self.file.owner, self.user)
        self.assertTrue(self.file.is_available)

class CompilationOptionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='testpass')
        CompilationOption.objects.create(standard='C89', optimization='nogcse', processor='MCS51', user=user)

    def test_compilation_option(self):
        option = CompilationOption.objects.get(id=1)
        self.assertEqual(option.standard, 'C89')
        self.assertEqual(option.optimization, 'nogcse')
        self.assertEqual(option.processor, 'MCS51')

class SectionTypeTestCase(TestCase):
    def setUp(self):
        SectionType.objects.create(type='procedure')

    def test_section_type(self):
        section_type = SectionType.objects.get(id=1)
        self.assertEqual(section_type.type, 'procedure')

class SectionStatusTestCase(TestCase):
    def setUp(self):
        SectionStatus.objects.create(status='compiles_with_warnings')

    def test_section_status(self):
        section_status = SectionStatus.objects.get(id=1)
        self.assertEqual(section_status.status, 'compiles_with_warnings')

class StatusDataTestCase(TestCase):
    def setUp(self):
        StatusData.objects.create(data='compilation_error')

    def test_status_data(self):
        status_data = StatusData.objects.get(id=1)
        self.assertEqual(status_data.data, 'compilation_error')

class FileSectionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='testpass')
        directory = Directory.objects.create(name='test_dir', owner=user)
        file = File.objects.create(name='test_file', directory=directory, content='Some text', owner=user)
        section_type = SectionType.objects.create(type='procedure')
        section_status = SectionStatus.objects.create(status='compiles_with_warnings')
        status_data = StatusData.objects.create(data='compilation_error')
        FileSection.objects.create(
            file=file,
            name='Some Name',
            description='Some Description',
            section_start=1,
            section_end=1,
            section_type=section_type,
            section_status=section_status,
            status_data=status_data,
            content='Some text'
        )

    def test_file_section(self):
        file_section = FileSection.objects.get(id=1)
        self.assertEqual(file_section.name, 'Some Name')
        self.assertEqual(file_section.description, 'Some Description')
        self.assertEqual(file_section.section_start, 1)
        self.assertEqual(file_section.section_end, 1)
        self.assertEqual(file_section.section_type.type, 'procedure')
        self.assertEqual(file_section.section_status.status, 'compiles_with_warnings')
        self.assertEqual(file_section.status_data.data, 'compilation_error')
        self.assertEqual(file_section.content, 'Some text')


from django.test import TestCase, Client
from .models import File, SectionType, SectionStatus, StatusData
from django.urls import reverse
from django.contrib.auth.models import User

class FileContentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(owner=self.user, name='Test directory')
        self.file = File.objects.create(owner=self.user, directory=self.directory, content='test content', compiled_content='compiled test content')
        self.section_type = SectionType.objects.create(type="procedure")
        self.section_status = SectionStatus.objects.create(status='compiles_with_warnings')
        self.status_data = StatusData.objects.create(data='compilation_error')

    def test_file_content(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('file_content', kwargs={'file_id': self.file.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test content')
        self.assertContains(response, 'compiled test content')

# class AddFileTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='12345')

#     def test_add_file(self):
#         self.client.login(username='testuser', password='12345')
#         # response = self.client.post(reverse('add_file'), {
#         #     'owner': self.user.id,
#         #     'content': 'This is a new file',
#         # })
#         #self.assertEqual(response.status_code, 302)  # expects a redirect after successful form submission
#         self.assertEqual(File.objects.last().content, 'This is a new file')

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import File
from django.forms.models import model_to_dict

class AddFileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.test_file_data = {
            'owner': self.user.id,
            'name': 'Test File',
            'content': 'This is a test file.'
        }

    def test_add_file(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_file'), self.test_file_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(File.objects.count(), 1)
        created_file = File.objects.first()
        created_file_dict = model_to_dict(created_file)
        for key, value in self.test_file_data.items():
            self.assertEqual(value, created_file_dict[key])  # Check if the created file's attributes match the posted data


class AddDirectoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_add_directory(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_directory'), {
            'owner': self.user.id,
            'name': 'New Directory',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Directory.objects.last().name, 'New Directory')

from .models import File
from django.shortcuts import get_object_or_404

class CompileAndUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(name='Test Directory', owner=self.user)  # Assuming these are the required fields for Directory
        self.file = File.objects.create(owner=self.user, directory=self.directory, content='test content', compiled_content='compiled test content')
        self.file = get_object_or_404(File, id=1)
        print("SELF>FILE>ID:")
        print(self.file.id)

    def test_compile_and_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('compile_and_update', kwargs={'file_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('compiled_content', str(response.content))


class UpdateCompilationOptionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.compilation_option = CompilationOption.objects.create(
            user=self.user,
            standard='c11', 
            optimization='noinvariant', 
            processor='z80'
        )

    def test_update_standard(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_standard'), {
            'standard': 'c11',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CompilationOption.objects.first().standard, 'c11')

    def test_update_optimization(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_optimization'), {
            'optimization': 'noinvariant',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CompilationOption.objects.first().optimization, 'noinvariant')

    def test_update_processor(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_processor'), {
            'processor': 'z80',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CompilationOption.objects.first().processor, 'z80')

class DeleteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.file = File.objects.create(owner=self.user, content='Test file', is_available=True)
        self.directory = Directory.objects.create(owner=self.user, name='Test directory', is_available=True)

    def test_delete_file_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_file'), {
            'file_id': self.file.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(File.objects.get(id=self.file.id).is_available, False)

    def test_delete_directory_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_directory'), {
            'directory_id': self.directory.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Directory.objects.get(id=self.directory.id).is_available, False)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import CompilationOption, Directory, File

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(owner=self.user, name='Test directory')

    def test_home_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.directory.name)

class MyLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_my_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, reverse('home'))

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_view(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser2', 'password1': '12345', 'password2': '12345', 'email': 'testuser2@gmail.com'})
        self.assertRedirects(response, reverse('login'))

class UpdateFileContentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(owner=self.user, name='Test directory')
        self.file = File.objects.create(owner=self.user, directory=self.directory, content='test content')

    def test_update_file_content(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_file_content'), {'file_id': self.file.id, 'file_content': 'updated content'})
        self.file.refresh_from_db()
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(self.file.content, 'updated content')



from django.test import TestCase
from django.contrib.auth.models import User
from core.models import CompilationOption, Directory, File
from core.forms import CompilationOptionForm, DirectoryForm, FileForm, SignUpForm

class CompilationOptionFormTest(TestCase):
    def test_form_valid(self):
        form = CompilationOptionForm(data={
            'standard': 'c11',
            'optimization': 'nogcse',
            'processor': 'z80'
        })
        self.assertTrue(form.is_valid())

class DirectoryFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_form_valid(self):
        form = DirectoryForm(data={
            'name': 'Test directory',
            'parent_directory': None,
            'last_modified': '2023-06-16T00:00:00Z'
        })
        self.assertTrue(form.is_valid())

class FileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.directory = Directory.objects.create(owner=self.user, name='Test directory')

    def test_form_valid(self):
        form = FileForm(data={
            'name': 'Test file',
            'directory': self.directory.id,
            'content': 'Test content',
            'compiled_content': 'Compiled test content',
            'last_modified': '2023-06-16T00:00:00Z'
        })
        self.assertTrue(form.is_valid())

class SignUpFormTest(TestCase):
    def test_form_valid(self):
        form = SignUpForm(data={
            'username': 'testuser2',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2@gmail.com',
            'password1': '12345',
            'password2': '12345'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = SignUpForm(data={
            'username': 'testuser2',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2@gmail.com',
            'password1': '12345',
            'password2': '123456'
        })
        self.assertFalse(form.is_valid())
