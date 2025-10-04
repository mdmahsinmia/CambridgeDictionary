// Function to play audio from URL - defined globally
function playAudio(url) {
    // Get the button that triggered the audio
    const button = event.currentTarget;
    const originalText = button.innerHTML;
    
    // Show loading state
    button.innerHTML = '⌛';
    button.disabled = true;
    
    const audio = new Audio(url);
    
    audio.addEventListener('canplaythrough', () => {
        // Reset button state
        button.innerHTML = originalText;
        button.disabled = false;
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            button.innerHTML = '❌';
            setTimeout(() => {
                button.innerHTML = originalText;
            }, 1000);
        });
    });
    
    audio.addEventListener('error', () => {
        console.error('Error loading audio:', audio.error);
        button.innerHTML = '❌';
        button.disabled = false;
        setTimeout(() => {
            button.innerHTML = originalText;
        }, 1000);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const wordInput = document.getElementById('word-input');
    const resultsContainer = document.getElementById('results-container');
    const loadingElement = document.getElementById('loading');
    
    // Only add event listener if search form exists (on dictionary page)
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const word = wordInput.value.trim();
            
            if (word) {
                // Show loading spinner
                resultsContainer.style.display = 'none';
                loadingElement.style.display = 'block';
                
                // Send request to backend
                const formData = new FormData();
                formData.append('word', word);
                
                fetch('/search', {
                    method: 'POST',
                    body: formData
                })
            .then(response => response.json())
            .then(data => {
                // Hide loading spinner
                loadingElement.style.display = 'none';
                resultsContainer.style.display = 'block';
                
                if (data.error) {
                    displayError(data.error);
                } else {
                    displayResults(data);
                }
            })
            .catch(error => {
                // Hide loading spinner
                loadingElement.style.display = 'none';
                resultsContainer.style.display = 'block';
                displayError('An error occurred while fetching the dictionary data.');
                console.error('Error:', error);
            });
        }
    });
}
    
    function displayResults(data) {
        // Clear previous results
        resultsContainer.innerHTML = '';
        
        // Create word header
        const wordHeader = document.createElement('div');
        wordHeader.className = 'word-header';
        
        const wordTitle = document.createElement('div');
        wordTitle.className = 'word-title';
        
        const wordHeading = document.createElement('h2');
        wordHeading.textContent = data.word;
        wordTitle.appendChild(wordHeading);
        
        if (data.pronunciation) {
            const pronunciationContainer = document.createElement('div');
            pronunciationContainer.className = 'pronunciation-container';
            
            const pronunciation = document.createElement('span');
            pronunciation.className = 'pronunciation';
            pronunciation.textContent = `/${data.pronunciation}/`;
            pronunciationContainer.appendChild(pronunciation);
            
            // Add audio button if audio URL is available
            if (data.audio_url) {
                const audioButton = document.createElement('button');
                audioButton.className = 'audio-button';
                audioButton.innerHTML = '🔊';
                audioButton.title = 'Listen to pronunciation';
                audioButton.addEventListener('click', function() {
                    const audio = new Audio(data.audio_url);
                    audio.play();
                });
                pronunciationContainer.appendChild(audioButton);
            }
            
            wordTitle.appendChild(pronunciationContainer);
        }
        
        wordHeader.appendChild(wordTitle);
        resultsContainer.appendChild(wordHeader);
        
        // Display each part of speech
        if (data.parts_of_speech && data.parts_of_speech.length > 0) {
            data.parts_of_speech.forEach(pos => {
                const posSection = document.createElement('div');
                posSection.className = 'part-of-speech';
                
                const posType = document.createElement('div');
                posType.className = 'pos-type';
                posType.textContent = pos.type;
                posSection.appendChild(posType);
                
                // Display definitions and examples
                if (pos.definitions && pos.definitions.length > 0) {
                    pos.definitions.forEach((def, index) => {
                        const definition = document.createElement('div');
                        definition.className = 'definition';
                        
                        const defText = document.createElement('div');
                        defText.className = 'definition-text';
                        defText.textContent = `${index + 1}. ${def.text}`;
                        definition.appendChild(defText);
                        
                        // Display examples
                        if (def.examples && def.examples.length > 0) {
                            const examples = document.createElement('div');
                            examples.className = 'examples';
                            
                            def.examples.forEach(example => {
                                const exampleEl = document.createElement('div');
                                exampleEl.className = 'example';
                                exampleEl.textContent = example;
                                examples.appendChild(exampleEl);
                            });
                            
                            definition.appendChild(examples);
                        }
                        
                        posSection.appendChild(definition);
                    });
                }
                
                resultsContainer.appendChild(posSection);
            });
        } else {
            const noDefinitions = document.createElement('div');
            noDefinitions.className = 'no-definitions';
            noDefinitions.textContent = 'No definitions found for this word.';
            resultsContainer.appendChild(noDefinitions);
        }
    }
    
    function displayError(message) {
        resultsContainer.innerHTML = `
            <div class="error-message">
                <p>${message}</p>
                <p>Please try another word or check your spelling.</p>
            </div>
            <div class="initial-message">
                <p>Enter a word to see its full Cambridge Dictionary entry</p>
            </div>
        `;
    }
});