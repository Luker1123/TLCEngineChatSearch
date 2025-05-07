import { useRef, useState, useEffect } from 'react';
import './App.css';





const examplePrompts = [
  'Vacation homes with beachfront property',
  'Ranch homes in Millburn, NJ',
  'Homes in walkable cities under $500,000',
  'Old homes with hardwood floors',
  'Houses with large backyards around $600,000',
  'Modern homes with lots of large windows',
];

function App() {
  const [searchText, setSearchText] = useState('');
  const [searching, setSearching] = useState(false);
  const [displayedExamples, setDisplayedExamples] = useState([]);
  const [logText, setLogText] = useState('');
  const [searchSubmitted, setSearchSubmitted] = useState(false);
  const textareaRef = useRef(null);

  useEffect(() => {
    const shuffled = examplePrompts.sort(() => 0.5 - Math.random());
    setDisplayedExamples(shuffled.slice(0, 3));
    document.body.style.visibility = 'visible';
  }, []);
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.scrollTop = textareaRef.current.scrollHeight;
    }
  }, [logText]); //runs every time logText updates

  const search = async (text, e) => {
    if (e) e.preventDefault();
    setSearching(true);
    const url = `http://localhost:5000/search?prompt=${encodeURIComponent(
      text
    )}`;
    //setFadingOut(true);
    // let test;
    // for(i=0;i<50;i++){
    //   test += 'hello\n';
    // }

    setLogText(
      `User input:\n${text}\n\nWaiting for response from server...\n`
    );
    const response = await fetch(url);
    const json = await response.json();
    setLogText((x) => `${x}Response:\n${JSON.stringify(json)}`);
    
    console.log(json);
    setSearching(false);
  };

  return (
    <><div id="all"
        className={`fade-in`}>
      <div className={`fade-on-submit ${searchSubmitted ? 'fade-out' : ''}`}>
      {/* {!searchSubmitted && <h1>What are you looking for?</h1>} */}
      <h1>What are you looking for?</h1>
      </div>
      <textarea id="chatBox" ref={textareaRef} readOnly rows='30' value={logText}></textarea>
      <form id='search-container' onSubmit={(e) => {
          e.preventDefault();
          search(searchText, e);
          setSearchSubmitted(true);
        }}>
        <div id='search-bar'>
          <input
            type='text'
            placeholder='Search'
            maxLength='100'
            value={searchText}
            disabled={searching}
            onInput={(e) => {
              setSearchText(e.target.value);
            }}
            autoFocus
          />
          <button type='submit' disabled={searching}>
            {searching ? 'Searching' : 'Search'}
          </button>
        </div>
        {/* {!searchSubmitted && (<div id='example-prompts'> */}
        {(<div
              id="example-prompts"
              className={`fade-on-submit ${searchSubmitted ? 'fade-out' : ''}`}
            >
          {displayedExamples.map((prompt, i) => (
            <div
              key={prompt}
              className={`example-prompt${searching ? ' disabled' : ''}`}
              style={{
                animationDelay: `${(i + 1) * 500}ms`,
              }}
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
        </div>)}
        
      </form>
      </div>
    </>
  );
}

export default App;
