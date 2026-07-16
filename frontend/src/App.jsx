import { useState } from "react";
import "./index.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const[count, setCount] = useState(0);

  async function search() {
  if(query.trim()===""){
    setResults([]);
    setCount(0);
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`
    );

    const data = await response.json();

    setResults(data.results);
    setCount(data.count);

  } catch (error) {
    console.error("Ошибка поиска:", error);
  } finally {
    setLoading(false);
  }
}


  return (
    <div className="container">

      <h1>🔎 SearchRIA</h1>
      <p className="subtitle">
          Поиск по новостям
      </p>

      <div className="search-box">

        <input
          placeholder="Введите запрос..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") search();
          }}
        />

        <button onClick={search}>
          Найти
        </button>

      </div>


      {loading && (
        <p className="loading">
          Ищем новости...
        </p>
      )}

      {!loading && query !== "" && (
          <p>
              Найдено результатов:
      <b>{count}</b>
          </p>
      )}

      {!loading && count === 0 && query !== "" && (
          <p> По вашему запросу ничего не найдено.</p>
      )}


      <div className="results">

        {results.map((post) => (

          <div className="card" key={post.post_id}>

            <div className="source">
                {post.source}
            </div>

            <div className="score">
                Релевантность: {post.score}
            </div>

            <div className="date">
                {new Date(post.date * 1000).toLocaleString("ru-RU")}
            </div>

            <p>
              {post.text.length > 400
                ? post.text.substring(0, 400) + "..."
                : post.text}
            </p>

            <a
              href={post.url}
              target="_blank"
              rel="noreferrer"
            >
            🔗 Открыть оригинал
            </a>

          </div>

        ))}

      </div>

    </div>
  );
}


export default App;