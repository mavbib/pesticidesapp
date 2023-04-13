
from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path
import numpy as np
from plotnine import ggplot, aes, geom_line, theme, element_text, labs

pesticides = pd.read_csv(Path(__file__).parent / "pesticides_use.csv")
pesticides['datetime'] = pd.to_datetime(pesticides['Year'], format='%Y')
pesticides.drop(axis=1, columns=['Year'], inplace=True)
result2 = type(pesticides['datetime'])
print(result2)

date_range_start = np.min(pesticides['datetime'])
date_range_end = np.max(pesticides["datetime"])
print(date_range_start)
result = type(date_range_start)
print(result)

print(date_range_start)
result = type(date_range_start)

static_content_url = "https://raw.githubusercontent.com/mavbib/pesticidesapp/main/pesticides_app/style"

area_names = pesticides['Area'].unique()
area_name_dict = {l: l for l in area_names}

app_ui = ui.page_fluid(
    ui.tags.head(

        ui.tags.link(rel="stylesheet", href="{static_content_url}/styles.css")),
    ui.tags.div(style="color: #444444;", children=[

        ui.panel_title("Pesticides Usage by Country")
    ]),
    ui.tags.body(
        ui.tags.div(style="background-color: #ffb265;", children=[
            ui.layout_sidebar(

                ui.panel_sidebar(ui.input_selectize(id="Area", label="Areas",
                                                    choices=area_name_dict, selected="Net Food Importing Developing Countries", multiple=True),
                                 ui.input_date_range(id="date_range", label="Date Range", start=date_range_start,
                                                     end=date_range_end),

                                 ),

                ui.panel_main(ui.output_plot("plottimeseries")
                              ),

            )]),
        ui.tags.p(
            "The data are from Food and Agriculture Organisation of the United Nations. Some figures are official and some are estimated"),
        ui.a("FAO.org", href="https://www.fao.org/home/en"),
        ui.tags.p(
            "Please note: adding country will change the scale of metric tonnes.")
    )
)


def server(input, output, session):

    @ reactive.Calc
    def lang_filt():
        date_selected_start = pd.to_datetime(input.date_range()[0])
        date_selected_end = pd.to_datetime(input.date_range()[1])
        lang_filt = pesticides.loc[(pesticides['Area'].isin(list(input.Area()))) & (
            pesticides['datetime'] >= date_selected_start) & (pesticides['datetime'] <= date_selected_end)].reset_index(drop=True)
        return lang_filt

    @ output
    @ render.plot
    def plottimeseries():
        g = ggplot(lang_filt(), aes(x="datetime", y="Tonnes")) + geom_line(aes(color="Area")) + labs(x='Years',
                                                                                                     y='Tonnes', title='Pesticides Usage Over Time')
        return g


# style = Path(__file__).parent / "style" static_assets=style
app = App(app_ui, server)
