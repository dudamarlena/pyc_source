# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/basketball_reference_web_scraper/client.py
# Compiled at: 2020-03-05 11:58:34
# Size of source mod 2**32: 7716 bytes
import requests
from basketball_reference_web_scraper import http_client
from basketball_reference_web_scraper.errors import InvalidSeason, InvalidDate, InvalidPlayerAndSeason
import basketball_reference_web_scraper.output as output
from basketball_reference_web_scraper.writers import CSVWriter, RowFormatter, BOX_SCORE_COLUMN_NAMES, SCHEDULE_COLUMN_NAMES, PLAYER_SEASON_TOTALS_COLUMN_NAMES, PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES, TEAM_BOX_SCORES_COLUMN_NAMES, PLAY_BY_PLAY_COLUMN_NAMES, PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES, SearchResultsCSVWriter, SEARCH_RESULTS_COLUMN_NAMES

def player_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.player_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidDate(day=day, month=month, year=year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=BOX_SCORE_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=BOX_SCORE_COLUMN_NAMES)),
      json_options=json_options)


def regular_season_player_box_scores(player_identifier, season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.regular_season_player_box_scores(player_identifier=player_identifier,
          season_end_year=season_end_year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.internal_server_error or http_error.response.status_code == requests.codes.not_found:
                raise InvalidPlayerAndSeason(player_identifier=player_identifier, season_end_year=season_end_year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=PLAYER_SEASON_BOX_SCORE_COLUMN_NAMES)),
      json_options=json_options)


def season_schedule(season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.season_schedule(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidSeason(season_end_year=season_end_year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=SCHEDULE_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=SCHEDULE_COLUMN_NAMES)),
      json_options=json_options)


def players_season_totals(season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.players_season_totals(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidSeason(season_end_year=season_end_year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=PLAYER_SEASON_TOTALS_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=PLAYER_SEASON_TOTALS_COLUMN_NAMES)),
      json_options=json_options)


def players_advanced_season_totals(season_end_year, include_combined_values=False, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.players_advanced_season_totals(season_end_year,
          include_combined_values=include_combined_values)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidSeason(season_end_year=season_end_year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=PLAYER_ADVANCED_SEASON_TOTALS_COLUMN_NAMES)),
      json_options=json_options)


def team_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.team_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidDate(day=day, month=month, year=year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=TEAM_BOX_SCORES_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=TEAM_BOX_SCORES_COLUMN_NAMES)),
      json_options=json_options)


def play_by_play(home_team, day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.play_by_play(home_team=home_team, day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        try:
            if http_error.response.status_code == requests.codes.not_found:
                raise InvalidDate(day=day, month=month, year=year)
            else:
                raise http_error
        finally:
            http_error = None
            del http_error

    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=CSVWriter(column_names=PLAY_BY_PLAY_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=PLAY_BY_PLAY_COLUMN_NAMES)),
      json_options=json_options)


def search(term, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    values = http_client.search(term=term)
    return output(values=values,
      output_type=output_type,
      output_file_path=output_file_path,
      output_write_option=output_write_option,
      csv_writer=SearchResultsCSVWriter(column_names=SEARCH_RESULTS_COLUMN_NAMES,
      row_formatter=RowFormatter(data_field_names=SEARCH_RESULTS_COLUMN_NAMES)),
      json_options=json_options)