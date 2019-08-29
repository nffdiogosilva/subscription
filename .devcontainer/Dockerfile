FROM nffdiogosilva/pytools

RUN mkdir /workspace
WORKDIR /workspace

# Install Python dependencies from Pipfile if it exists
COPY Pipfile /workspace/
RUN if [ -f "Pipfile" ]; then pipenv lock --clear && pipenv install --dev --verbose --system --deploy; fi

# Install git, process tools
RUN apt-get update && apt-get -y install git procps

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
