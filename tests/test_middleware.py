from django.http import QueryDict, HttpResponse
from django.test import RequestFactory
from hamcrest import equal_to, assert_that, same_instance, calling, raises
from hamcrest.core.base_matcher import BaseMatcher
from emulate_aws_env.middleware import modify_request


test_response = HttpResponse()
middleware_handler = modify_request(lambda r: test_response)

request_factory = RequestFactory()


def test_request_removes_qs_dupes():
    request = request_factory.get('/', data={'name': ['1', '2']})

    response = middleware_handler(request)

    assert_that(request.GET.urlencode(), equal_to('name=2'))
    assert_that(request.META['QUERY_STRING'], equal_to('name=2'))
    assert_that(request.environ['QUERY_STRING'], equal_to('name=2'))
    assert_that(response, same_instance(test_response))


def test_request_leaves_valid_qs():
    request = request_factory.get('/', data={'animal': 'dog', 'sport': 'soccer'})

    response = middleware_handler(request)

    assert_that(request.GET, matches_query_string('animal=dog&sport=soccer'))
    assert_that(request.META['QUERY_STRING'], matches_query_string('animal=dog&sport=soccer'))
    assert_that(request.environ['QUERY_STRING'], matches_query_string('animal=dog&sport=soccer'))
    assert_that(response, same_instance(test_response))


def test_wsgi_request_throws_exception_for_content_too_large():
    too_large_size = 10485761
    request = request_factory.post('/', data={'': ''.join('x' * (too_large_size - 83))})
    assert request.META['CONTENT_LENGTH'] == too_large_size

    assert_that(calling(lambda: middleware_handler(request)), raises(Exception))


def test_wsgi_request_proceeds_for_content_exact_size():
    too_large_size = 10485760
    request = request_factory.post('/', data={'': ''.join('x' * (too_large_size - 83))})
    assert request.META['CONTENT_LENGTH'] == too_large_size

    response = middleware_handler(request)

    assert_that(response, same_instance(test_response))


class MatchesQueryString(BaseMatcher):
    def __init__(self, qs):
        self.qs = qs

    def _matches(self, item):
        if isinstance(item, QueryDict):
            item_qs = item
        else:
            item_qs = QueryDict(str(item))
        return item_qs == QueryDict(self.qs)

    def describe_to(self, description):
        description.append_text('query string equivalent to ').append_text(self.qs)


def matches_query_string(qs):
    return MatchesQueryString(qs)
