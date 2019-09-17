def paginate(func):
    """
    Paginate Decorator: Returns a slice from the whole list attending to the page_size and page_number parameters
    :param func: Decorated function
    :return: The paginator function
    """

    async def paginator(*args, **kwargs):
        """
        Paginator: Paginates a list and returns the corresponding page. If the page doesn't exist returns an empty
        list. If the page exists but can't be filled with enough elements returns the existing part of that page.
        :param args: args passed to the decorated function
        :param kwargs: **kwargs passed to the decorated function and page_size and page_number args
        :return: A slice from the whole list of size page_size or lower
        """
        query_result = await func(*args)
        page_number, page_size = kwargs['page_number'], kwargs['page_size']
        start = (page_number - 1) * page_size
        end = page_number * page_size
        # Full page
        if len(query_result) > end:
            idxs = slice(start, end)
            return query_result[idxs]
        # Partial page
        elif len(query_result) > start:
            idxs = slice(start, len(query_result))
            return query_result[idxs]
        # Empty page
        else:
            return []

    return paginator


def serialize(func):
    """
    Serialize Decorator: decorates query results serializing the result.
    :param func: Decorated function
    :return: The serializer function
    """

    async def serializer(*args, **kwargs):
        """
        Serializer: Calls the serialize method on a single beer or on every beer from a list of beers
        :param args: args passed to the decorated function
        :param kwargs: kwargs passed to the decorated function
        :return: A serialized beer or a list of serialized beers
        """
        result = await func(*args, **kwargs)
        return list(map(lambda beer: beer.serialize(), result)) if isinstance(result, list) else result.serialize()

    return serializer


def sort(func):
    """
    Sort decorator: sorts query results attending to criteria
    :param func: Decorated function
    :return: The sorter function
    """

    async def sorter(*args, **kwargs):
        """
        Sorter: Sorts the list attending to the query
        :param args: args passed to the decorated function
        :param kwargs: kwargs passed to the decorated function which contain the query options
        :return: A sorted list of beers
        """
        result = func(*args, **kwargs)
        return result

    return sorter
