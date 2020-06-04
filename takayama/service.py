from sqlalchemy import desc, func
from takayama.models import Scrobble
from takayama.tmpd import TakayamaMpdClient


def engine(group_by, agg, filtering, limit, options_string):
    options = options_string.split(',')
    mpd_is_enabled = 'mpd' in options

    q = Scrobble.query
    filters_and = filtering.split(',')
    filters = [f.split('=') for f in filters_and]
    for f in filters:
        field_name = f[0]
        field_value = f[1]
        field = {
            'year': Scrobble.played_year,
            'month': Scrobble.played_month,
            'day': Scrobble.played_day,
            'name': Scrobble.name
        }.get(field_name, None)
        if field is not None:
            q = q.filter(field == field_value)

    group_bys = group_by.split(',')
    group_fields = []
    for gb in group_bys:
        group_by_field = {
            'artist': Scrobble.artist,
            'name': Scrobble.name,
            'album': Scrobble.album
        }.get(gb, None)
        if group_by_field is not None:
            group_fields.append(group_by_field)

    aggregates = agg.split(',')
    aggregate_expressions = []
    for aggregate in aggregates:
        agg_expression = {
            'count': func.count(1)
        }.get(aggregate, None)
        if agg_expression is not None:
            aggregate_expressions.append(agg_expression)

    q = q.from_self(*group_fields, *aggregate_expressions)

    if group_fields:
        q = q.group_by(*group_fields)
    if aggregate_expressions:
        q = q.order_by(*[desc(a) for a in aggregate_expressions])

    scrobbles = q.limit(limit).all()

    if mpd_is_enabled:
        with TakayamaMpdClient() as takayama_mpd:
            takayama_mpd.clear_playlist()
            for scrobble in scrobbles:
                if hasattr(scrobble, 'name') and hasattr(scrobble, 'artist') and scrobble.name and scrobble.artist:
                    takayama_mpd.add_tracks_by_artist(scrobble.artist, scrobble.name)

    return scrobbles
