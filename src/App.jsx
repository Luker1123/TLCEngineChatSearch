import { useState, useEffect } from 'react';
import './App.css';

const examplePrompts = [
  "Vacation homes with beachfront property",
  "Ranch homes in Millburn, NJ",
  "Homes in walkable cities under $500,000",
  "Old homes with hardwood floors",
  "Houses with large backyards around $600,000",
  "Modern homes with lots of large windows",
];

function App() {

  const [searchText, setSearchText] = useState('');
  const [searching, setSearching] = useState(false);
  const [displayedExamples, setDisplayedExamples] = useState([]);
  useEffect(() => {
    const shuffled = examplePrompts.sort(() => 0.5 - Math.random());
    setDisplayedExamples(shuffled.slice(0, 3));
  }, []);

  const search = async (text, e) => {
    if (e) e.preventDefault();
    setSearching(true);
    console.log(`user prompt: ${text}`);
    await new Promise(resolve => setTimeout(resolve, 2000));

    /* 
    const url = ``;
    const response = await fetch(url);
    const json = await response.json();
    console.log(json); 
    */
    setSearching(false);
  };

  return (
    <>
      <h1>What are you looking for?</h1>
      <form id="search-container" onSubmit={(e) => search(searchText, e)}>
        <div id="search-bar">
          <input
            type="text" 
            placeholder="Search"
            maxLength="100"
            value={searchText}
            disabled={searching}
            onInput={(e) => {
              setSearchText(e.target.value);
            }} 
            autoFocus
          />
          <button
            type="submit"
            disabled={searching}
          >Search</button>
        </div>
        <div id="example-prompts">
        {displayedExamples.map((prompt, i) => (
          <div 
            key={prompt} 
            className="example-prompt"
            style={{ animationDelay: `${(i + 1) * 500}ms`}}
            title={`Search for "${prompt}"`}
            onClick={() => {
              setSearchText(prompt);
              search(prompt);
            }}
          >"{prompt}"</div>
        ))}
      </div>
      </form>
    </>
  );
}

export default App
