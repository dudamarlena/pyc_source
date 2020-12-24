# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/management/commands/fill-database.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os, random, string, sys
from optparse import make_option
from django import db
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.db import transaction
from django.utils import six
from reviewboard.accounts.models import Profile
from reviewboard.reviews.forms import UploadDiffForm
from reviewboard.diffviewer.models import DiffSetHistory
from reviewboard.reviews.models import ReviewRequest, Review, Comment
from reviewboard.scmtools.models import Repository, Tool
NORMAL = 1
DESCRIPTION_SIZE = 100
SUMMARY_SIZE = 6
LOREM_VOCAB = [
 b'Lorem', b'ipsum', b'dolor', b'sit', b'amet', b'consectetur',
 b'Nullam', b'quis', b'erat', b'libero.', b'Ut', b'vel', b'velit', b'augue, ',
 b'risus.', b'Curabitur', b'dignissim', b'luctus', b'dui, ', b'et',
 b'tristique', b'id.', b'Etiam', b'blandit', b'adipiscing', b'molestie.',
 b'libero', b'eget', b'lacus', b'adipiscing', b'aliquet', b'ut', b'eget',
 b'urna', b'dui', b'auctor', b'id', b'varius', b'eget', b'consectetur',
 b'Sed', b'ornare', b'fermentum', b'erat', b'ut', b'consectetur', b'diam',
 b'in.', b'Aliquam', b'eleifend', b'egestas', b'erat', b'nec', b'semper.',
 b'a', b'mi', b'hendrerit', b'vestibulum', b'ut', b'vehicula', b'turpis.',
 b'habitant', b'morbi', b'tristique', b'senectus', b'et', b'netus', b'et',
 b'fames', b'ac', b'turpis', b'egestas.', b'Vestibulum', b'purus', b'odio',
 b'quis', b'consequat', b'non, ', b'vehicula', b'nec', b'ligula.', b'In',
 b'ipsum', b'in', b'volutpat', b'ipsum.', b'Morbi', b'aliquam', b'velit',
 b'molestie', b'suscipit.', b'Morbi', b'dapibus', b'nibh', b'vel',
 b'justo', b'nibh', b'facilisis', b'tortor, ', b'sit', b'amet', b'dictum',
 b'amet', b'arcu.', b'Quisque', b'ultricies', b'justo', b'non', b'neque',
 b'nibh', b'tincidunt.', b'Curabitur', b'sit', b'amet', b'sem', b'quis',
 b'vulputate.', b'Mauris', b'a', b'lorem', b'mi.', b'Donec', b'dolor',
 b'interdum', b'eu', b'scelerisque', b'vel', b'massa.', b'Vestibulum',
 b'risus', b'vel', b'ipsum', b'suscipit', b'laoreet.', b'Proin', b'congue',
 b'blandit.', b'Aenean', b'aliquet', b'auctor', b'nibh', b'sit', b'amet',
 b'Vestibulum', b'ante', b'ipsum', b'primis', b'in', b'faucibus', b'orci',
 b'posuere', b'cubilia', b'Curae;', b'Donec', b'lacinia', b'tincidunt',
 b'facilisis', b'nisl', b'eu', b'fermentum.', b'Ut', b'nec', b'laoreet',
 b'magna', b'egestas', b'nulla', b'pharetra', b'vel', b'egestas', b'tellus',
 b'Pellentesque', b'sed', b'pharetra', b'orci.', b'Morbi', b'eleifend, ',
 b'interdum', b'placerat,', b'mi', b'dolor', b'mollis', b'libero',
 b'quam', b'posuere', b'nisl.', b'Vivamus', b'facilisis', b'aliquam',
 b'condimentum', b'pulvinar', b'egestas.', b'Lorem', b'ipsum', b'dolor',
 b'consectetur', b'adipiscing', b'elit.', b'In', b'hac', b'habitasse',
 b'Aenean', b'blandit', b'lectus', b'et', b'dui', b'tincidunt', b'cursus',
 b'Suspendisse', b'ipsum', b'dui, ', b'accumsan', b'eget', b'imperdiet',
 b'est.', b'Integer', b'porta, ', b'ante', b'ac', b'commodo', b'faucibus',
 b'molestie', b'risus, ', b'a', b'imperdiet', b'eros', b'neque', b'ac',
 b'nisi', b'leo', b'pretium', b'congue', b'eget', b'quis', b'arcu.', b'Cras']
NAMES = [
 b'Aaron', b'Abbey', b'Adan', b'Adelle', b'Agustin', b'Alan', b'Aleshia',
 b'Alexia', b'Anderson', b'Ashely', b'Barbara', b'Belen', b'Bernardo',
 b'Bernie', b'Bethanie', b'Bev', b'Boyd', b'Brad', b'Bret', b'Caleb',
 b'Cammy', b'Candace', b'Carrol', b'Charlette', b'Charlie', b'Chelsea',
 b'Chester', b'Claude', b'Daisy', b'David', b'Delila', b'Devorah',
 b'Edwin', b'Elbert', b'Elisha', b'Elvis', b'Emmaline', b'Erin',
 b'Eugene', b'Fausto', b'Felix', b'Foster', b'Garrett', b'Garry',
 b'Garth', b'Gracie', b'Henry', b'Hertha', b'Holly', b'Homer',
 b'Ileana', b'Isabella', b'Jacalyn', b'Jaime', b'Jeff', b'Jefferey',
 b'Jefferson', b'Joie', b'Kanesha', b'Kassandra', b'Kirsten', b'Kymberly',
 b'Lashanda', b'Lean', b'Lonnie', b'Luis', b'Malena', b'Marci', b'Margarett',
 b'Marvel', b'Marvin', b'Mel', b'Melissia', b'Morton', b'Nickole', b'Nicky',
 b'Odette', b'Paige', b'Patricia', b'Porsche', b'Rashida', b'Raul',
 b'Renaldo', b'Rickie', b'Robbin', b'Russel', b'Sabine', b'Sabrina',
 b'Sacha', b'Sam', b'Sasha', b'Shandi', b'Sherly', b'Stacey', b'Stephania',
 b'Stuart', b'Talitha', b'Tanesha', b'Tena', b'Tobi', b'Tula', b'Valene',
 b'Veda', b'Vikki', b'Wanda', b'Wendie', b'Wendolyn', b'Wilda', b'Wiley',
 b'Willow', b'Yajaira', b'Yasmin', b'Yoshie', b'Zachariah', b'Zenia',
 b'Allbert', b'Amisano', b'Ammerman', b'Androsky', b'Arrowsmith',
 b'Bankowski', b'Bleakley', b'Boehringer', b'Brandstetter',
 b'Capehart', b'Charlesworth', b'Danforth', b'Debernardi',
 b'Delasancha', b'Denkins', b'Edmunson', b'Ernsberger', b'Faupel',
 b'Florence', b'Frisino', b'Gardner', b'Ghormley', b'Harrold',
 b'Hilty', b'Hopperstad', b'Hydrick', b'Jennelle', b'Massari',
 b'Solinski', b'Swisher', b'Talladino', b'Tatham', b'Thornhill',
 b'Ulabarro', b'Welander', b'Xander', b'Xavier', b'Xayas', b'Yagecic',
 b'Yagerita', b'Yamat', b'Ying', b'Yurek', b'Zaborski', b'Zeccardi',
 b'Zecchini', b'Zimerman', b'Zitzow', b'Zoroiwchak', b'Zullinger', b'Zyskowski']

class Command(NoArgsCommand):
    help = b'Populates the database with the specified fields'
    option_list = BaseCommand.option_list + (
     make_option(b'-u', b'--users', type=b'int', default=None, dest=b'users', help=b'The number of users to add'),
     make_option(b'--review-requests', default=None, dest=b'review_requests', help=b'The number of review requests per user [min:max]'),
     make_option(b'--diffs', default=None, dest=b'diffs', help=b'The number of diff per review request [min:max]'),
     make_option(b'--reviews', default=None, dest=b'reviews', help=b'The number of reviews per diff [min:max]'),
     make_option(b'--diff-comments', default=None, dest=b'diff_comments', help=b'The number of comments per diff [min:max]'),
     make_option(b'-p', b'--password', type=b'string', default=None, dest=b'password', help=b'The login password for users created'))

    @transaction.atomic
    def handle_noargs(self, users=None, review_requests=None, diffs=None, reviews=None, diff_comments=None, password=None, verbosity=NORMAL, **options):
        num_of_requests = None
        num_of_diffs = None
        num_of_reviews = None
        num_of_diff_comments = None
        random.seed()
        if review_requests:
            num_of_requests = self.parse_command(b'review_requests', review_requests)
            repo_dir = os.path.abspath(os.path.join(sys.argv[0], b'..', b'scmtools', b'testdata', b'git_repo'))
            if not os.path.exists(repo_dir):
                raise CommandError(b'No path to the repository')
            self.repository = Repository.objects.create(name=b'Test Repository', path=repo_dir, tool=Tool.objects.get(name=b'Git'))
        if diffs:
            num_of_diffs = self.parse_command(b'diffs', diffs)
            diff_dir_tmp = os.path.abspath(os.path.join(sys.argv[0], b'..', b'reviews', b'management', b'commands', b'diffs'))
            if not os.path.exists(diff_dir_tmp):
                raise CommandError(b'Diff dir does not exist')
            diff_dir = diff_dir_tmp + b'/'
            files = [ f for f in os.listdir(diff_dir) if f.endswith(b'.diff')
                    ]
            if len(files) == 0:
                raise CommandError(b'No diff files in this directory')
        if reviews:
            num_of_reviews = self.parse_command(b'reviews', reviews)
        if diff_comments:
            num_of_diff_comments = self.parse_command(b'diff-comments', diff_comments)
        if not users:
            raise CommandError(b'At least one user must be added')
        for i in range(1, users + 1):
            new_user = User.objects.create(username=self.rand_username(), first_name=random.choice(NAMES), last_name=random.choice(NAMES), email=b'test@example.com', is_staff=False, is_active=True, is_superuser=False)
            if password:
                new_user.set_password(password)
                new_user.save()
            else:
                new_user.set_password(b'test1')
                new_user.save()
            Profile.objects.create(user=new_user, first_time_setup_done=True, collapsed_diffs=True, wordwrapped_diffs=True, syntax_highlighting=True, show_closed=True)
            req_val = self.pick_random_value(num_of_requests)
            if int(verbosity) > NORMAL:
                self.stdout.write(b'For user %s:%s' % (i, new_user.username))
                self.stdout.write(b'=============================')
            for j in range(0, req_val):
                if int(verbosity) > NORMAL:
                    self.stdout.write(b'Request #%s:' % j)
                review_request = ReviewRequest.objects.create(new_user, None)
                review_request.public = True
                review_request.summary = self.lorem_ipsum(b'summary')
                review_request.description = self.lorem_ipsum(b'description')
                review_request.shipit_count = 0
                review_request.repository = self.repository
                if j == 0:
                    review_request.target_people.add(User.objects.get(pk=1))
                review_request.save()
                diff_val = self.pick_random_value(num_of_diffs)
                if diff_val > 0:
                    diffset_history = DiffSetHistory.objects.create(name=b'testDiffFile' + six.text_type(i))
                    diffset_history.save()
                for k in range(0, diff_val):
                    if int(verbosity) > NORMAL:
                        self.stdout.write(b'%s:\tDiff #%s' % (i, k))
                    random_number = random.randint(0, len(files) - 1)
                    file_to_open = diff_dir + files[random_number]
                    f = open(file_to_open, b'r')
                    form = UploadDiffForm(review_request=review_request, files={b'path': File(f)})
                    if form.is_valid():
                        cur_diff = form.create(f, None, diffset_history)
                    review_request.diffset_history = diffset_history
                    review_request.save()
                    review_request.publish(new_user)
                    f.close()
                    review_val = self.pick_random_value(num_of_reviews)
                    for l in range(0, review_val):
                        if int(verbosity) > NORMAL:
                            self.stdout.write(b'%s:%s:\t\tReview #%s:' % (
                             i, j, l))
                        reviews = Review.objects.create(review_request=review_request, user=new_user)
                        reviews.publish(new_user)
                        comment_val = self.pick_random_value(num_of_diff_comments)
                        for m in range(0, comment_val):
                            if int(verbosity) > NORMAL:
                                self.stdout.write(b'%s:%s:\t\t\tComments #%s' % (
                                 i, j, m))
                            if m == 0:
                                file_diff = cur_diff.files.order_by(b'id')[0]
                            max_lines = 220
                            first_line = random.randrange(1, max_lines - 1)
                            remain_lines = max_lines - first_line
                            num_lines = random.randrange(1, remain_lines)
                            diff_comment = Comment.objects.create(filediff=file_diff, text=b'comment number %s' % (m + 1), first_line=first_line, num_lines=num_lines)
                            review_request.publish(new_user)
                            reviews.comments.add(diff_comment)
                            reviews.save()
                            reviews.publish(new_user)
                            db.reset_queries()

                        if comment_val == 0:
                            db.reset_queries()

                    if review_val == 0:
                        db.reset_queries()

                if diff_val == 0:
                    db.reset_queries()

            if req_val == 0:
                db.reset_queries()
            if req_val != 0:
                self.stdout.write(b'user %s created with %s requests' % (
                 new_user.username, req_val))
            else:
                self.stdout.write(b'user %s created successfully' % new_user.username)

        return

    def parse_command(self, com_arg, com_string):
        """Parse the values given in the command line."""
        try:
            return tuple(int(item.strip()) for item in com_string.split(b':'))
        except ValueError:
            raise CommandError(b'You failed to provide "%s" with one or two values of type int.\nExample: --%s=2:5' % (
             com_arg, com_arg))

    def rand_username(self):
        """Used to generate random usernames so no flushing needed."""
        return (b'').join(random.choice(string.ascii_lowercase) for x in range(0, random.randrange(5, 9)))

    def pick_random_value(self, value):
        """Pick a random value out of a range.

        If the 'value' tuple is empty, this returns 0. If 'value' contains a
        single number, this returns that number. Otherwise, this returns a
        random number between the two given numbers.
        """
        if not value:
            return 0
        if len(value) == 1:
            return value[0]
        return random.randrange(value[0], value[1])

    def lorem_ipsum(self, ipsum_type):
        """Create some random text for summary/description."""
        if ipsum_type == b'description':
            max_size = DESCRIPTION_SIZE
        else:
            max_size = SUMMARY_SIZE
        return (b' ').join(random.choice(LOREM_VOCAB) for x in range(0, max_size))