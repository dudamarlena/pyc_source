# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/policy.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging
from rbpowerpack.hostingsvcs.feature import AWSCodeCommitFeature, BitbucketServerFeature, GitHubEnterpriseFeature, VisualStudioTeamServicesFeature
from rbpowerpack.pdf.feature import PDFReviewFeature
from rbpowerpack.reports.feature import ReportsFeature
from rbpowerpack.scmtools.feature import TFSFeature

class ExtensionPolicy(object):
    """Calculates policies for the extension.

    This is used to determine whether different features of Power Pack can
    be used, or even if Power Pack itself can be used, for a given user and
    the license.

    This determines whether features can be used based on the license validity
    and the configured FeaturePolicy class.
    """

    def __init__(self, extension):
        self.extension = extension
        self.feature_policy = None
        return

    def load_feature_policy(self):
        """Loads the FeaturePolicy for Power Pack.

        This can be set in settings, but will default to the built-in
        FeaturePolicy class.
        """
        self.feature_policy = FeaturePolicy(self.extension)
        feature_policy_path = self.extension.settings[b'feature_policy_path']
        if feature_policy_path:
            try:
                i = feature_policy_path.rfind(b'.')
                module_name = feature_policy_path[:i]
                cls_name = feature_policy_path[i + 1:]
                mod = __import__(module_name, {}, {}, [cls_name])
                cls = getattr(mod, cls_name)
                self.feature_policy = cls(self)
            except Exception as e:
                logging.error(b'Unable to load Power Pack feature policy class: %s', e, exc_info=1)

    def is_aws_codecommit_enabled(self, user, repository):
        """Return whether AWS CodeCommit is enabled for the given user.

        By default, it is enabled for all licensed users (so long as the
        feature itself is enabled in settings). Subclasses can override this to
        create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user to check.

            repository (reviewboard.scmtools.models.Repository):
                The repository being verified.

        Returns:
            bool:
            True if the given user is allowed to use AWS CodeCommit.
        """
        return self.extension.features[AWSCodeCommitFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_aws_codecommit_enabled(user, repository)

    def is_bitbucket_server_enabled(self, user, repository):
        """Return whether Bitbucket Server is enabled for the given user.

        By default, it is enabled for all licensed users (so long as the
        feature itself is enabled in settings). Subclasses can override this to
        create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user to check.

            repository (reviewboard.scmtools.models.Repository):
                The repository being verified.

        Returns:
            bool:
            True if the given user is allowed to use Bitbucket Server.
        """
        return self.extension.features[BitbucketServerFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_bitbucket_server_enabled(user, repository)

    def is_github_enterprise_enabled(self, user, repository):
        """Return whether GitHub Enterprise is enabled for the given user.

        By default, it is enabled for all licensed users (so long as the
        feature itself is enabled in settings). Subclasses can override this to
        create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change, based on license
            settings. ``False`` if they cannot.
        """
        return self.extension.features[GitHubEnterpriseFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_github_enterprise_enabled(user, repository)

    def is_pdf_enabled(self, user, review_request):
        """Return whether PDF review is enabled for a user and review request.

        This will check if the license is valid, PDF is enabled in settings, if
        the user is permitted in the license, and if the FeaturePolicy allows
        PDF to be used.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The review request that the PDF document is attached to.

        Returns:
            bool:
            ``True`` if the user can access PDF review, based on license
            settings. ``False`` if they cannot.
        """
        return self.extension.features[PDFReviewFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_pdf_enabled(user, review_request)

    def is_reporting_enabled(self, user, local_site_name=None):
        """Return whether reporting is enabled for the given user.

        By default, it is enabled for all licensed users (so long as the
        feature itself is enabled in settings). Subclasses can override this to
        create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            local_site_name (unicode):
                The name of the current local site.

        Returns:
            bool:
            ``True`` if the user can access reports, based on license settings.
            ``False`` if they cannot.
        """
        return self.extension.features[ReportsFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_reporting_enabled(user, local_site_name)

    def is_tfs_enabled(self, user, repository):
        """Return whether TFS is enabled for a given user.

        This includes both TFS and TFS-Git.

        It is enabled for all licensed users (so long as the feature itself is
        enabled in settings). Feature policy classes can augment this.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            repository (reviewboard.scmtools.models.Repository):
                The TFS repository.

        Returns:
            bool:
            The enabled state for TFS.
        """
        return self.extension.features[TFSFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_tfs_enabled(user, repository)

    def is_visual_studio_team_services_enabled(self, user, repository):
        """Return whether Visual Studio Team Services is enabled for the user.

        By default, it is enabled for all users (so long as the feature itself
        is enabled in settings). Subclasses can override this to create custom
        behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change, based on license
            settings. ``False`` if they cannot.
        """
        return self.extension.features[VisualStudioTeamServicesFeature].enabled and self._is_license_valid(user) and self.feature_policy.is_visual_studio_team_services_enabled(user, repository)

    def _is_license_valid(self, user):
        """Return whether the license is valid for the given user.

        This will return True if there's an installed license that's still
        valid that either has no cap or is licensed to the user.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

        Returns:
            bool:
            Whether the current license is valid and includes the user.
        """
        license = self.extension.license
        return license and license.valid and (not license.has_user_cap or self.extension.license_settings.is_user_licensed(user))


class FeaturePolicy(object):
    """Calculates policies for different features of Power Pack.

    This is used to determine if features can be enabled for a given user or
    review request.

    This is used by ExtensionPolicy to determine if a feature can be enabled in
    that install. By default, all features can be enabled, but this can be
    overridden in specialized installs (primarily RBCommons) to lock down Power
    Pack in special ways.
    """

    def __init__(self, extension):
        self.extension = extension

    def is_aws_codecommit_enabled(self, user, repository):
        """Return whether AWS CodeCommit is enabled for a user and repository.

        By default, it is always enabled for all users and repositories (so
        long as the feature itself is enabled in settings). Subclasses can
        override this to create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change. ``False`` if they cannot.
        """
        return True

    def is_bitbucket_server_enabled(self, user, repository):
        """Return whether Bitbucket Server is enabled for a user and repository.

        By default, it is always enabled for all users and repositories (so
        long as the feature itself is enabled in settings). Subclasses can
        override this to create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change. ``False`` if they cannot.
        """
        return True

    def is_github_enterprise_enabled(self, user, repository):
        """Return whether GitHub Enterprise is enabled for the given user.

        By default, it is enabled for all users (so long as the feature itself
        is enabled in settings). Subclasses can override this to create custom
        behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change. ``False`` if they cannot.
        """
        return True

    def is_pdf_enabled(self, user, review_request):
        """Return whether PDF review is enabled for a user and review request.

        By default, it is always enabled for all users and review requests
        (so long as the feature itself is enabled in settings). Subclasses
        can override this to create custom behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The review request that the PDF document is attached to.

        Returns:
            bool:
            ``True`` if the user can access PDF review. ``False`` if they
            cannot.
        """
        return True

    def is_reporting_enabled(self, user, local_site_name):
        """Return whether reporting is enabled for the given user.

        By default, it is enabled for all users (so long as the feature itself
        is enabled in settings). Subclasses can override this to create custom
        behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            local_site_name (unicode):
                The name of the current local site.

        Returns:
            bool:
            ``True`` if the user can access reports. ``False`` if they cannot.
        """
        return True

    def is_tfs_enabled(self, user, repository):
        """Return whether TFS is enabled for the given user.

        This includes both TFS and TFS-Git.

        By defaut, this returns ``True``, always, leveraging the built-in
        behavior in :py:class:`ExtensionPolicy`. Subclasses can override
        this to augment the logic.

        Args:
            user (django.contrib.auth.models.User):
                The user being checked.

            repository (reviewboard.scmtools.models.Repository):
                The TFS repository.

        Returns:
            bool:
            ``True`` if the user can post a change. ``False`` if they cannot.
        """
        return True

    def is_visual_studio_team_services_enabled(self, user, repository):
        """Return whether Visual Studio Team Services is enabled for the user.

        By default, it is enabled for all users (so long as the feature itself
        is enabled in settings). Subclasses can override this to create custom
        behavior.

        Args:
            user (django.contrib.auth.models.User):
                The user accessing something for the repository.

            repository (reviewboard.scmtools.models.Repository):
                The repository being accessed.

        Returns:
            bool:
            ``True`` if the user can post a change. ``False`` if they cannot.
        """
        return True