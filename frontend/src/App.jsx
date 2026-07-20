import { useState } from "react";
import "./index.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const[count, setCount] = useState(0);

  const [mode, setMode] = useState("search");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  async function search() {
  if(query.trim()===""){
    setResults([]);
    setCount(0);
    return;
  }

  setLoading(true);
  setAnswer("");
  setSources([]);

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

  async function ask() {
  if(query.trim()===""){
    setAnswer("");
    setSources([]);
    return;
  }

  setLoading(true);
  setResults([]);
  setCount(0);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/ask?q=${encodeURIComponent(query)}`
    );

    const data = await response.json();

    setAnswer(data.answer);
    setSources(data.sources);

  } catch (error) {
    console.error("Ошибка запроса:", error);
    setAnswer("Не удалось получить ответ. Проверьте, что сервер запущен.");
  } finally {
    setLoading(false);
  }
}

  function handleSubmit() {
    if (mode === "search") {
      search();
    } else {
      ask();
    }
  }


  return (
    <div className="container">

      <h1>🔎 SearchRIA</h1>
      <p className="subtitle">
          Поиск по новостям
      </p>

      <div className="mode-switch">
        <button
          className={mode === "search" ? "active" : ""}
          onClick={() => setMode("search")}
        >
          Поиск
        </button>
        <button
          className={mode === "ask" ? "active" : ""}
          onClick={() => setMode("ask")}
        >
          Спросить
        </button>
      </div>

      <div className="search-box">

        <input
          placeholder={mode === "search" ? "Введите запрос..." : "Задайте вопрос..."}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSubmit();
          }}
        />

        <button onClick={handleSubmit}>
          {mode === "search" ? "Найти" : "Спросить"}
        </button>

      </div>


      {loading && (
        <p className="loading">
          {mode === "search" ? "Ищем новости..." : "Формируем ответ..."}
        </p>
      )}

      {!loading && mode === "ask" && answer !== "" && (
        <div className="answer-box">
          <p>{answer}</p>

          {sources.length > 0 && (
            <div className="answer-sources">
              <p><b>Источники:</b></p>
              {sources.map((src, i) => (
                <a
                  key={i}
                  href={src.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  🔗 Источник {i + 1} (релевантность: {src.score})
                </a>
              ))}
            </div>
          )}
        </div>
      )}

      {!loading && mode === "search" && query !== "" && (
          <p>
              Найдено результатов:
      <b>{count}</b>
          </p>
      )}

      {!loading && mode === "search" && count === 0 && query !== "" && (
          <p> По вашему запросу ничего не найдено.</p>
      )}


      <div className="results">

        {mode === "search" && results.map((post) => (

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