import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
    const interval = setInterval(fetchReviews, 5000); // auto-refresh
    return () => clearInterval(interval);
  }, []);

  async function fetchReviews() {
    try {
      const response = await axios.get("/api/reviews");
      setReviews(response.data);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>WhatsApp Product Reviews</h1>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "20px",
          }}
        >
          <thead>
            <tr>
              <th style={thStyle}>User</th>
              <th style={thStyle}>Product</th>
              <th style={thStyle}>Review</th>
              <th style={thStyle}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {reviews.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ padding: "10px", textAlign: "center" }}>
                  No reviews yet.
                </td>
              </tr>
            ) : (
              reviews.map((review) => (
                <tr key={review.id}>
                  <td style={tdStyle}>{review.user_name}</td>
                  <td style={tdStyle}>{review.product_name}</td>
                  <td style={tdStyle}>{review.product_review}</td>
                  <td style={tdStyle}>
                    {review.created_at
                      ? new Date(review.created_at).toLocaleString()
                      : "-"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

const thStyle = {
  textAlign: "left",
  borderBottom: "2px solid #ddd",
  padding: "8px",
  fontSize: "16px",
};

const tdStyle = {
  borderBottom: "1px solid #eee",
  padding: "8px",
  fontSize: "14px",
};

export default App;