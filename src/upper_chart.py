import altair as alt
from src import theme


def create_upper_chart(df, pts, genres, ratings, year_from, year_to):
    """Create upper chart.

    Parameters
    ----------
    df : DataFrame
       Source data
    genres : list
       List of genres
    ratings : list
       List of MPAA ratings
    year_from : string
       Starting year
    year_to : string
       Ending year

    Returns
    -------
    Chart :
        Altair chart
    """
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', theme.mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')

    # filtering df based on genre
    df_genre = df[df.Major_Genre.isin(genres)]

    # filtering df_genre based on rating
    df_rating = df_genre[df_genre.MPAA_Rating.isin(ratings)]

    # filtering df_rating based on the year range
    start_year = int(year_from)
    end_year = int(year_to)
    df_year = df_rating.query('Release_Year >= @start_year and Release_Year <= @end_year').dropna()

    top_us_gross_df = (df_year[df_year['US_Gross']
                       .notnull()]
                       .sort_values("US_Gross", ascending=False)
                       .head(10))

    top_gross = alt.Chart(top_us_gross_df).transform_calculate(
        gross_revenue_per_million="datum.US_Gross/1000000"
    ).encode(
        y=alt.Y("Title:N", title=None,
                sort=alt.EncodingSortField(
                    field="gross_revenue_per_million",
                    order="descending"),
                axis=alt.Axis(labelLimit=300)),
        tooltip=[alt.Tooltip("Release_Year:N",
                             title="Year"),
                 alt.Tooltip("Major_Genre:N",
                             title="Genre"),
                 alt.Tooltip("MPAA_Rating:N",
                             title="MPAA Rating"),
                 alt.Tooltip("gross_revenue_per_million:Q",
                             title="Gross Revenue (millions)",
                             format=".2f")],
    ).properties(
        title="Highest Grossing US Movies",
    )

    top_us_gross_chart = top_gross.mark_bar(
    ).encode(
        alt.X("gross_revenue_per_million:Q", title="Gross Revenue (millions of USD)"),
        color=alt.condition(
            pts,
            alt.Color("Title:O", scale=alt.Scale(scheme="set1"), legend=None),
            alt.ColorValue("grey"))
    ).add_selection(pts)

    return top_us_gross_chart.interactive()
