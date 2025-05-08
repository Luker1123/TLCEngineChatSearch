import { useRef, useState, useEffect } from 'react';
import './App.css';

const examplePrompts = [
  'Old homes with no garage, 2 bedroom 2 bath in East Brunswick',
];

function App() {
  const [searchText, setSearchText] = useState('');
  const [searching, setSearching] = useState(false);
  const [displayedExamples, setDisplayedExamples] = useState([]);
  const [logHtml, setLogHtml] = useState('');
  const [searchSubmitted, setSearchSubmitted] = useState(false);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    const shuffled = examplePrompts.sort(() => 0.5 - Math.random());
    setDisplayedExamples(shuffled.slice(0, 3));
    document.body.style.visibility = 'visible';
  }, []);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [logHtml]);

  const isImageUrl = (url) => /\.(jpeg|jpg|gif|png|webp)$/i.test(url);

  const search = async (text, e) => {
    if (e) e.preventDefault();
    setSearching(true);

    try {
      const url = `http://localhost:5001/search?prompt=${encodeURIComponent(text)}`;
      const response = await fetch(url);
      const tex2 = await response.text();

      let previewHtml = '';

      if (isImageUrl(tex2)) {
        previewHtml = `<img src="${tex2}" alt="Snapshot" style="max-width:100%; margin-top: 1rem;" />`;
      } else {
        previewHtml = `
          <div style="margin-top:1rem;">
            <br/>
            <iframe 
              src="${tex2}" 
              title="Web snapshot" 
              style="width:100%; height:500px; border:1px solid #ccc; border-radius:8px;"
            ></iframe>
            <br/>
            <a href="${tex2}" target="_blank">${tex2}</a>
          </div>
        `;
      }

      setLogHtml((prev) => `${prev}<br/><strong>Response</strong><br/>${previewHtml}`);
    } catch (err) {
      setLogHtml((prev) => `${prev}<br/><span style="color:red;">❌ Error fetching data.</span>`);
    }

    setSearching(false);
  };

  return (
    <div id="all" className="fade-in" style={{ padding: '2rem' }}>
      <div className={`fade-on-submit ${searchSubmitted ? 'fade-out' : ''}`}>
        <h1>What are you looking for?</h1>
      </div>

      <div
        id="chatBox"
        ref={chatBoxRef}
        className="chat-box"
        dangerouslySetInnerHTML={{ __html: logHtml }}
      ></div>

      <form
        id="search-container"
        onSubmit={(e) => {
          e.preventDefault();
          search(searchText, e);
          setSearchSubmitted(true);
        }}
      >
        <div id="search-bar">
          <input
            type="text"
            placeholder="Search"
            maxLength="100"
            value={searchText}
            disabled={searching}
            onInput={(e) => setSearchText(e.target.value)}
            autoFocus
          />
          <button type="submit" disabled={searching}>
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div
          id="example-prompts"
          className={`fade-on-submit ${searchSubmitted ? 'fade-out' : ''}`}
        >
          {displayedExamples.map((prompt, i) => (
            <div
              key={prompt}
              className={`example-prompt${searching ? ' disabled' : ''}`}
              style={{ animationDelay: `${(i + 1) * 500}ms` }}
              title={`Search for "${prompt}"`}
              onClick={() => {
                if (searching) return;
                setSearchText(prompt);
                search(prompt);
                setSearchSubmitted(true);
              }}
            >
              "{prompt}"
            </div>
          ))}
        </div>
      </form>
    </div>
  );
}

export default App;
