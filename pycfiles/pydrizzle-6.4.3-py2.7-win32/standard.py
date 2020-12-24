# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\standard.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from traits import Trait
from trait_handlers import TraitString, TraitPrefixList, TraitEnum, TraitList
from trait_base import trait_editors
trait_editors = trait_editors()
if trait_editors:
    boolean_editor = trait_editors.TraitEditorBoolean()
else:
    boolean_editor = None
false_trait = Trait(False, TraitEnum(False, True), editor=boolean_editor)
true_trait = Trait(True, false_trait)
flexible_true_trait = Trait('true', {'true': 1, 't': 1, 'yes': 1, 'y': 1, 'on': 1, 1: 1, 'false': 0, 
   'f': 0, 'no': 0, 'n': 0, 'off': 0, 0: 0}, editor=boolean_editor)
flexible_false_trait = Trait('false', flexible_true_trait)
zipcode_5_trait = Trait('99999', TraitString(regex='^\\d{5,5}$'))
zipcode_9_trait = Trait('99999-9999', TraitString(regex='^\\d{5,5}[ -]?\\d{4,4}$'))
us_states_long_trait = Trait('Texas', TraitPrefixList([
 'Alabama', 'Alaska', 'Arizona', 'Arkansas',
 'California', 'Colorado', 'Connecticut', 'Delaware',
 'Florida', 'Georgia', 'Hawaii', 'Idaho',
 'Illinois', 'Indiana', 'Iowa', 'Kansas',
 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
 'Missouri', 'Montana', 'Nebraska', 'Nevada',
 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
 'South Dakota', 'Tennessee', 'Texas', 'Utah',
 'Vermont', 'Virginia', 'Washington', 'West Virginia',
 'Wisconsin', 'Wyoming']))
us_states_short_trait = Trait('TX', [
 'AL', 'AK', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
 'HI', 'ID', 'IA', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
 'ME', 'MI', 'MO', 'MN', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
 'NJ', 'NM', 'NY', 'NV', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])
all_us_states_long_trait = Trait('Texas', TraitPrefixList([
 'Alabama', 'Alaska', 'American Samoa', 'Arizona',
 'Arkansas', 'California', 'Colorado', 'Connecticut',
 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
 'Guam', 'Hawaii', 'Idaho', 'Illinois',
 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
 'South Dakota', 'Tennessee', 'Texas', 'Utah',
 'Vermont', 'Virgin Islands', 'Virginia', 'Washington',
 'West Virginia', 'Wisconsin', 'Wyoming']))
all_us_states_short_trait = Trait('TX', [
 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC',
 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI',
 'VA', 'WA', 'WV', 'WI', 'WY'])
countries_long_trait = Trait('United States', TraitPrefixList([
 'Afghanistan', 'Albania', 'Algeria', 'Andorra',
 'Angola', 'Antigua and Barbuda', 'Argentina',
 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
 'Belarus', 'Belgium', 'Belize', 'Benin',
 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
 'Botswana', 'Brazil', 'Brunei', 'Bulgaria',
 'Burkina Faso', 'Burma/Myanmar', 'Burundi', 'Cambodia',
 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic',
 'Chad', 'Chile', 'China', 'Colombia',
 'Comoros', 'Congo', 'Democratic Republic of Congo',
 'Costa Rica', "Cote d'Ivoire/Ivory Coast", 'Croatia',
 'Cuba', 'Cyprus', 'Denmark', 'Djibouti',
 'Dominica', 'Dominican Republic', 'East Timor',
 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea',
 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji',
 'Finland', 'France', 'Gabon', 'Gambia',
 'Georgia', 'Germany', 'Ghana', 'Greece',
 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau',
 'Guyana', 'Haiti', 'Honduras', 'Hungary',
 'Iceland', 'India', 'Indonesia', 'Iran',
 'Iraq', 'Ireland', 'Israel', 'Italy',
 'Jamaica', 'Japan', 'Jordan', 'Kazakstan',
 'Kenya', 'Kiribati', 'North Korea', 'South Korea',
 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia',
 'Madagascar', 'Malawi', 'Malaysia', 'Maldives',
 'Mali', 'Malta', 'Marshall Islands',
 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia',
 'Moldova', 'Monaco', 'Mongolia', 'Morocco',
 'Mozambique', 'Namibia', 'Nauru', 'Nepal',
 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger',
 'Nigeria', 'Norway', 'Oman', 'Pakistan',
 'Palau', 'Panama', 'Papua New Guinea',
 'Paraguay', 'Peru', 'Philippines', 'Poland',
 'Portugal', 'Qatar', 'Romania',
 'Russian Federation East of the Ural Mountains',
 'Russian Federation West of the Ural Mountains', 'Rwanda',
 'Saint Kitts and Nevis', 'Saint Lucia',
 'Saint Vincent and the Grenadines', 'Samoa',
 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia',
 'Senegal', 'Seychelles', 'Sierra Leone',
 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands',
 'Somalia', 'South Africa', 'Spain', 'Sri Lanka',
 'Sudan', 'Suriname', 'Swaziland', 'Sweden',
 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
 'Tanzania', 'Thailand', 'Togo', 'Tonga',
 'Trinidad and Tobago', 'Tunisia', 'Turkey',
 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine',
 'United Arab Emirates', 'United Kingdom',
 'United States', 'Uruguay', 'Uzbekistan',
 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam',
 'Yemen', 'Yugoslavia', 'Zambia', 'Zimbabwe']))
month_long_trait = Trait('January', TraitPrefixList([
 'January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']), cols=2)
month_short_trait = Trait('Jan', [
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], cols=2)
day_of_week_long_trait = Trait('Sunday', TraitPrefixList([
 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
 'Saturday']), cols=1)
day_of_week_short_trait = Trait('Sun', [
 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], cols=1)
phone_short_trait = Trait('555-1212', TraitString(regex='^\\d{3,3}[ -]?\\d{4,4}$'))
phone_long_trait = Trait('800-555-1212', TraitString(regex='^\\d{3,3}[ -]?\\d{3,3}[ -]?\\d{4,4}$|^\\(\\d{3,3}\\) ?\\d{3,3}[ -]?\\d{4,4}$'))
ssn_trait = Trait('000-00-0000', TraitString(regex='^\\d{3,3}[ -]?\\d{2,2}[ -]?\\d{4,4}$'))
string_list_trait = Trait([], TraitList(''))
int_list_trait = Trait([], TraitList(0))
float_list_trait = Trait([], TraitList(0.0))
complex_list_trait = Trait([], TraitList(complex(0.0, 1.0)))