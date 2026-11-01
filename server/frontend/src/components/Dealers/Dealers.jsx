import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [originalDealers, setOriginalDealers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const get_dealers = async () => {
    try {
      setLoading(true);
      const res = await fetch("/djangoapp/get_dealers");
      if (!res.ok) throw new Error("Unable to load dealerships.");
      const data = await res.json();
      if (data.status === 200 && Array.isArray(data.dealers)) {
        setOriginalDealers(data.dealers);
        setDealersList(data.dealers);
      } else {
        setError(data.message || "No dealership data was returned.");
      }
    } catch (err) {
      setError(err.message || "Unable to load dealerships.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);
    setDealersList(originalDealers.filter(dealer =>
      (dealer.state || "").toLowerCase().includes(query.toLowerCase())
    ));
  };

  const handleLostFocus = () => {
    if (!searchQuery.trim()) setDealersList(originalDealers);
  };

  useEffect(() => { get_dealers(); }, []);

  const isLoggedIn = sessionStorage.getItem("username") !== null;
  return (
    <div>
      <Header />
      <main style={{ padding: "24px" }}>
        <h2>Find a dealership</h2>
        <label htmlFor="state-search">Filter by state</label>
        <input id="state-search" type="text" placeholder="Search states..." value={searchQuery}
          onChange={handleInputChange} onBlur={handleLostFocus}
          style={{ display: "block", padding: "10px", margin: "10px 0 20px", maxWidth: "320px", width: "100%" }} />
        {loading && <p>Loading dealerships…</p>}
        {error && <p role="alert">{error}</p>}
        {!loading && !error && <table className="table">
          <thead><tr><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th>{isLoggedIn && <th>Review Dealer</th>}</tr></thead>
          <tbody>{dealersList.map(dealer => <tr key={dealer.id}>
            <td>{dealer.id}</td><td><a href={'/dealer/' + dealer.id}>{dealer.full_name}</a></td>
            <td>{dealer.city}</td><td>{dealer.address}</td><td>{dealer.zip}</td><td>{dealer.state}</td>
            {isLoggedIn && <td><a href={'/postreview/' + dealer.id}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>}
          </tr>)}</tbody>
        </table>}
      </main>
    </div>
  );
};
export default Dealers;
