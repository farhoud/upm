FROM openjdk:8-jre-alpine



RUN addgroup -g 1000 docker && \
    adduser -u 1000 -G docker -h /home/docker -s /bin/sh -D docker

USER docker:docker

RUN apk add --no-cache --quiet \
    bash \
    curl

ENV NEO4J_SHA256=0e5c6492cd274edf06c5f10d2b64711bd559aaff37c646e03bfa65e613994174 \
    NEO4J_TARBALL=neo4j-community-3.3.1-unix.tar.gz \
    NEO4J_EDITION=community
ARG NEO4J_URI=http://dist.neo4j.org/neo4j-community-3.3.1-unix.tar.gz

COPY ./local-package/* /tmp/

RUN curl --fail --silent --show-error --location --remote-name ${NEO4J_URI} \
    && echo "${NEO4J_SHA256}  ${NEO4J_TARBALL}" | sha256sum -csw - \
    && tar --extract --file ${NEO4J_TARBALL} --directory /var/lib \
    && mv /var/lib/neo4j-* /var/lib/neo4j \
    && rm ${NEO4J_TARBALL} \
    && mv /var/lib/neo4j/data /data \
    && ln -s /data /var/lib/neo4j/data \
    && apk del curl

ENV PATH /var/lib/neo4j/bin:$PATH

WORKDIR /var/lib/neo4j

VOLUME /data

COPY docker-entrypoint.sh /docker-entrypoint.sh

EXPOSE 7474 7473 7687

RUN apk add --no-cache curl

RUN USER=docker && \
    GROUP=docker && \
    /usr/bin/curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.2/fixuid-0.2-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\n" > /etc/fixuid/config.yml



ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["neo4j"]
