FROM mambaorg/micromamba:1.5.10

COPY envs/longread_qc.yml /tmp/env.yml

RUN micromamba create -y -n longread_qc -f /tmp/env.yml && micromamba clean -a -y

ENV PATH=/opt/conda/envs/longread_qc/bin:$PATH

WORKDIR /work