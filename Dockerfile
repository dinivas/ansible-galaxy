# vim: set ft=Dockerfile:


FROM centos:7

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV PIP_NO_CACHE_DIR off
ENV GALAXY_VENV /usr/share/galaxy/venv

# Install packages and create virtual environment
RUN yum -y install epel-release \
    && yum -y install git gcc make python36 python36-devel \
    && yum -y clean all \
    && rm -rf /var/cache/yum

# Install python dependencies
COPY requirements/requirements.txt /tmp/requirements.txt
RUN python3.6 -m venv ${GALAXY_VENV} \
    && "${GALAXY_VENV}/bin/pip" install -U \
        'pip' \
        'wheel' \
        'setuptools' \
    && "${GALAXY_VENV}/bin/pip" install -r /tmp/requirements.txt

RUN mkdir -p /galaxy
COPY . /galaxy
RUN "${GALAXY_VENV}/bin/pip" install -q -e '/galaxy/'

# Install tini
ENV TINI_VERSION v0.18.0
RUN curl -sL -o '/usr/local/bin/tini' \
        "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
    && chmod +x /usr/local/bin/tini \
    && yum -y clean all \
    && rm -rf /var/cache/yum

# Create galaxy user
ENV HOME /var/lib/galaxy
RUN mkdir -p /var/lib/galaxy \
    && useradd --system --gid root --home-dir "${HOME}" galaxy

# Create directories structure
RUN mkdir -p /etc/galaxy \
             /usr/share/galaxy/public \
             /var/lib/galaxy/media \
             /var/run/galaxy \
             /var/tmp/galaxy/imports \
             /var/tmp/galaxy/uploads

COPY scripts/docker/release/entrypoint.sh /entrypoint
# COPY --from=galaxy-builder /galaxy/dist/VERSION /usr/share/galaxy/
# COPY --from=galaxy-builder /galaxy/dist/*.whl /tmp
# RUN _galaxy_wheel="/tmp/galaxy-$(< /usr/share/galaxy/VERSION)-py3-none-any.whl" \
#     && "${GALAXY_VENV}/bin/pip" install "${_galaxy_wheel}" \
#     && rm -f "${_galaxy_wheel}"


# Fix directory permissions
RUN chown -R galaxy:root \
        /etc/galaxy \
        /usr/share/galaxy \
        /var/lib/galaxy \
        /var/run/galaxy \
        /var/tmp/galaxy \
    && chmod -R u=rwX,g=rwX\
        /etc/galaxy \
        /usr/share/galaxy \
        /var/lib/galaxy \
        /var/run/galaxy \
        /var/tmp/galaxy

VOLUME ["/var/lib/galaxy", "/var/tmp/galaxy"]

WORKDIR /var/lib/galaxy

ENV DJANGO_SETTINGS_MODULE galaxy.settings.production
# Workaround for git running under different users
# See https://github.com/jenkinsci/docker/issues/519
ENV GIT_COMMITTER_NAME 'Ansible Galaxy'
ENV GIT_COMMITTER_EMAIL 'galaxy@ansible.com'

USER galaxy
EXPOSE 8000

ENTRYPOINT ["/entrypoint"]
CMD ["run", "api"]