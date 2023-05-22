from django.test import TestCase
from django.db.utils import IntegrityError

from api.articles.models import Draft
from api.articles.models import Article
from api.articles.models import Published
from api.users.models import User


# Create your tests here.


class PublishedArticleTestCase(TestCase):
    def setUp(self) -> None:
        # user
        self.username = "jma"
        self.password = "markymarky"
        self.email_address = "marky@gmail.com"

        # article
        self.title = "A quick brown fox"
        self.content = "jumps over the lazy dog"

        self.author = User.objects.create(
            username=self.username,
            password=self.password,
            email_address=self.email_address,
        )

    def test_create_published_article(self):
        article = Article.objects.create(title=self.title, content=self.content)
        Published.objects.create(author=self.author, article=article)

    def test_get_published_article(self):
        # create published
        article = Article.objects.create(title=self.title, content=self.content)
        Published.objects.create(author=self.author, article=article)

        published = Published.objects.get(author=self.author)
        assert published.author.username == self.username
        assert published.author.email_address == self.email_address

    def test_update_published_article(self):
        # create published
        article = Article.objects.create(title=self.title, content=self.content)
        published = Published.objects.create(author=self.author, article=article)

        published_id = published.pk

        # update published
        to_update = Published.objects.get(id=published_id)
        to_update.article.title = "A slow white bear"
        to_update.article.save()

        # get published for verifying the update
        updated = Published.objects.get(id=published_id)

        assert updated.article.title == "A slow white bear"

    def test_duplicate_published_article(self):
        article = Article.objects.create(title=self.title, content=self.content)
        Published.objects.create(author=self.author, article=article)

        article = Article.objects.create(title=self.title, content=self.content)
        Published.objects.create(author=self.author, article=article)


class DraftArticleTestCase(TestCase):
    def setUp(self) -> None:
        # user
        self.username = "jma"
        self.password = "markymarky"
        self.email_address = "marky@gmail.com"

        # article
        self.title = "A quick brown fox"
        self.content = "jumps over the lazy dog"

        self.author = User.objects.create(
            username=self.username,
            password=self.password,
            email_address=self.email_address,
        )

    def test_create_draft_article(self):
        article = Article.objects.create(title=self.title, content=self.content)
        Draft.objects.create(author=self.author, article=article)

    def test_get_draft_article(self):
        # create draft
        article = Article.objects.create(title=self.title, content=self.content)
        Draft.objects.create(author=self.author, article=article)

        draft = Draft.objects.get(author=self.author)
        assert draft.author.username == self.username
        assert draft.author.email_address == self.email_address

    def test_update_draft_article(self):
        # create draft
        article = Article.objects.create(title=self.title, content=self.content)
        draft = Draft.objects.create(author=self.author, article=article)

        draft_id = draft.pk

        # update draft
        to_update = Draft.objects.get(id=draft_id)
        to_update.article.title = "A slow white bear"
        to_update.article.save()

        # get draft for verifying the update
        updated = Draft.objects.get(id=draft_id)

        assert updated.article.title == "A slow white bear"

    def test_duplicate_draft_article(self):
        article = Article.objects.create(title=self.title, content=self.content)
        Draft.objects.create(author=self.author, article=article)

        article = Article.objects.create(title=self.title, content=self.content)
        Draft.objects.create(author=self.author, article=article)
