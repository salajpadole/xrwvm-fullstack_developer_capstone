import React, { useState, useEffect, useCallback } from "react";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const get_dealers = useCallback(async (state = "") => {
    try {
      setLoading(true);
      setError("");
      const url = state.trim()
        ? `/djangoapp/get_dealers/${encodeURIComponent(state.trim())}`
        : "/djangoapp/get_dealers";
      const res = await fetch(url);
      const data = await res.json();
      if (!res.ok || data.status !== 200 || !Array.isArray(data.dealers)) {
        throw new Error(data.message || "Unable to load dealerships.");
      }
      setDealersList(data.dealers);
    } catch (err) {
      setError(err.message || "Unable to load dealerships.");
      setDealersList([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { get_dealers(); }, [get_dealers]);

  const handleInputChange = (event) => {
    const value = event.target.value;
    setSearchQuery(value);
    get_dealers(value);
  };

  const isLoggedIn = sessionStorage.getItem("username") !== null;

  return (
    <div>
      <Header />
      <main style={{ padding: "24px" }}>
        <h2>Find a dealership</h2>
        <label htmlFor="state-search">Filter by state</label>
        <input
          id="state-search"
          type="text"
          placeholder="Search states..."
          value={searchQuery}
          onChange={handleInputChange}
          style={{ display: "block", padding: "10px", margin: "10px 0 20px", maxWidth: "320px", width: "100%" }}
        />
        {loading && <p>Loading dealerships…</p>}
        {error && <p role="alert">{error}</p>}
        {!loading && !error && (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th>
                {isLoggedIn && <th>Review Dealer</th>}
              </tr>
            </thead>
            <tbody>
              {dealersList.map(dealer => (
                <tr key={dealer.id}>
                  <td>{dealer.id}</td>
                  <td><a href={"/dealer/" + dealer.id}>{dealer.full_name}</a></td>
                  <td>{dealer.city}</td><td>{dealer.address}</td><td>{dealer.zip}</td><td>{dealer.state}</td>
                  {isLoggedIn && <td><a href={"/postreview/" + dealer.id}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>}
                </tr>
              ))}
              {dealersList.length === 0 && <tr><td colSpan={isLoggedIn ? 7 : 6}>No dealerships found.</td></tr>}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
};

export default Dealers;
