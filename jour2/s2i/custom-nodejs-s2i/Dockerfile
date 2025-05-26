FROM registry.access.redhat.com/ubi8/nodejs-14

LABEL io.k8s.description="Custom Node.js S2I builder with additional tools" \
      io.k8s.display-name="Node.js 14 Custom S2I builder" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"

USER root
RUN dnf install -y git wget curl && \
    mv /usr/libexec/s2i/assemble /usr/libexec/s2i/assemble.original && \
    mv /usr/libexec/s2i/run /usr/libexec/s2i/run.original && \
    dnf clean all

COPY .s2i/bin/ /usr/libexec/s2i/
RUN chmod +x /usr/libexec/s2i/*
RUN echo 'hello'
USER 1001
CMD ["/usr/libexec/s2i/usage"]