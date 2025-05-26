FROM registry.access.redhat.com/ubi8/openjdk-17

LABEL io.k8s.description="Custom Java S2I builder with Maven" \
      io.k8s.display-name="Java 17 with Maven" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"

USER root

RUN microdnf install -y maven && microdnf clean all

COPY .s2i/bin/ /usr/libexec/s2i/
RUN chmod +x /usr/libexec/s2i/*

USER 1001

CMD ["/usr/libexec/s2i/usage"]
