document.addEventListener('DOMContentLoaded', function() {
    const sourceButtons = document.querySelectorAll('.source');
    const observerConfigs = document.querySelectorAll('[id$="_sourceConfig"]');
    const analyzerButtons = document.querySelectorAll('.analyzer');
    const analyzerConfigs = document.querySelectorAll('[id$="_analyzer"]');
    const sinkButtons = document.querySelectorAll('.sink');
    const sinkConfigs = document.querySelectorAll('[id$="_sink"]');

    // Event listener for source buttons
    sourceButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;

            // Hide all observer configs
            observerConfigs.forEach(config => {
                config.style.display = 'none';
            });

            // Show the observer config corresponding to the clicked source button
            const configElement = document.getElementById(targetId);
            if (configElement) {
                configElement.style.display = 'block';
            }
        });
    });

    // Event listener for analyzer buttons
    analyzerButtons.forEach(button => {
        button.addEventListener('click', () => {
            const analyzer = button.dataset.analyzer;

            // Hide all analyzer configs
            analyzerConfigs.forEach(config => {
                config.style.display = 'none';
            });

            // Show the analyzer config corresponding to the clicked button
            const configElement = document.getElementById(analyzer);
            if (configElement) {
                configElement.style.display = 'block';
            }
        });
    });

    // Event listener for sink buttons
    sinkButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sink = button.dataset.sink;

            // Hide all sink configs
            sinkConfigs.forEach(config => {
                config.style.display = 'none';
            });

            // Show the sink config corresponding to the clicked button
            const configElement = document.getElementById(sink);
            if (configElement) {
                configElement.style.display = 'block';
            }
        });
    });

    // Event listener for submitting report
    document.getElementById('submitReport').addEventListener('click', async () => {
        const selectedSource = document.querySelector('.source.selected').dataset.source;
        const selectedAnalyzer = document.querySelector('.analyzer.selected').dataset.analyzer;
        const selectedSink = document.querySelector('.sink.selected').dataset.sink;

        const sourceConfig = getSourceConfig(selectedSource);
        const analyzerConfig = getAnalyzerConfig(selectedAnalyzer);
        const sinkConfig = getSinkConfig(selectedSink);

        const config = {
            source: sourceConfig,
            analyzer: analyzerConfig,
            sink: sinkConfig
        };

        try {
            const response = await fetch('/create_report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    source: selectedSource,
                    analyzer: selectedAnalyzer,
                    sink: selectedSink,
                    config: config
                })
            });

            if (response.ok) {
                const result = await response.json();
                alert('Report created successfully with ID: ' + result.id);
            } else {
                throw new Error('Failed to create report');
            }
        } catch (error) {
            alert(error.message);
        }
    });
});

function getSourceConfig(source) {
    switch(source) {
        case 'twitter_source':
            return {
                query: document.getElementById('query').value,
                lookupPeriod: document.getElementById('lookupPeriod').value,
                maxTweets: document.getElementById('maxTweets').value,
                consumerKey: document.getElementById('consumerKey').value,
                consumerSecret: document.getElementById('consumerSecret').value
            };
        // Add other sources similarly
        default:
            return {};
    }
}

function getAnalyzerConfig(analyzer) {
    switch(analyzer) {
        case 'classification_analyzer':
            return {
                labels: document.getElementById('classification_labels').value,
                multiClass: document.getElementById('classification_multi_class').value,
                model: document.getElementById('classification_model').value,
                device: document.getElementById('device').value
            };
        // Add other analyzers similarly
        default:
            return {};
    }
}

function getSinkConfig(sink) {
    switch(sink) {
        case 'zendesk_sink':
            return {
                domain: document.getElementById('domain').value,
                subdomain: document.getElementById('subdomain').value,
                email: document.getElementById('emailSource').value,
                password: document.getElementById('password').value
            };
        // Add other sinks similarly
        default:
            return {};
    }
}
