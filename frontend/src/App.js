
import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import "./App.css";
import Login from "./Login";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

//  Backend Basic Auth 
const AUTH_HEADER = {
  Authorization: "Basic " + btoa("admin:admin123"),
};

function App() {
  
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [summary, setSummary] = useState(null);
  const [equipments, setEquipments] = useState([]);
  const [history, setHistory] = useState([]);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [hasUploaded, setHasUploaded] = useState(false);

  const fetchHistory = () => {
    fetch("http://127.0.0.1:8000/api/upload-history/", {
      headers: AUTH_HEADER,
    })
      .then((res) => res.json())
      .then((data) => setHistory(data))
      .catch((err) => console.error("Error fetching history:", err));
  };


  const fetchDashboardData = () => {
    fetch("http://127.0.0.1:8000/api/summary/", {
      headers: AUTH_HEADER,
    })
      .then((res) => res.json())
      .then((data) => setSummary(data));

    fetch("http://127.0.0.1:8000/api/equipment/", {
      headers: AUTH_HEADER,
    })
      .then((res) => res.json())
      .then((data) => setEquipments(data));
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchHistory();
    }
  }, [isLoggedIn]);


  const handleUpload = () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/api/upload/", {
      method: "POST",
      headers: AUTH_HEADER,
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message || "Upload successful");
        setHasUploaded(true);
        fetchDashboardData();
        fetchHistory();
      })
      .catch(() => alert("Upload failed"));
  };


  const generatePDF = () => {
    if (!summary) return;
    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text("Chemical Equipment Report", 14, 20);

    doc.setFontSize(11);
    doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30);

    doc.setFontSize(14);
    doc.text("Summary Metrics", 14, 45);

    doc.setFontSize(11);
    doc.text(`Total Equipment: ${summary.total_equipment}`, 14, 55);
    doc.text(`Avg Flowrate: ${summary.averages?.avg_flowrate}`, 14, 62);
    doc.text(`Avg Pressure: ${summary.averages?.avg_pressure}`, 14, 69);
    doc.text(`Avg Temperature: ${summary.averages?.avg_temperature}`, 14, 76);

    autoTable(doc, {
      startY: 90,
      head: [["Name", "Type", "Flowrate", "Pressure", "Temperature"]],
      body: equipments.map((eq) => [
        eq.name,
        eq.equipment_type,
        eq.flowrate,
        eq.pressure,
        eq.temperature,
      ]),
    });

    doc.save("chemical_equipment_report.pdf");
  };

  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="container">
      <div className="header">
        <div className="header-title">
          <h1>Chemical Equipment Dashboard</h1>
          <p>Real-time industrial monitoring and analytics</p>
        </div>
        <button className="logout-btn" onClick={() => setIsLoggedIn(false)}>
          Logout
        </button>
      </div>

      {/* --- CSV Upload Section --- */}
      <div className="card">
        <h2>Upload Data</h2>
        <div className="upload-container">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={handleUpload}>Process CSV</button>
        </div>
        {message && <p className="success-msg">{message}</p>}
      </div>

      {/* --- History Section --- */}
      <div className="card">
        <h2>Recent Activity</h2>
        <div className="history-grid">
          {history.length > 0 ? (
            history.map((item, index) => (
              <div className="history-card" key={index}>
                <p className="history-date">📅 {item.uploaded_at}</p>
                <p><strong>Total:</strong> {item.total_equipment}</p>
                <p><strong>Avg Flow:</strong> {item.avg_flowrate}</p>
              </div>
            ))
          ) : (
            <p>No recent uploads found.</p>
          )}
        </div>
      </div>

      {/* --- Dynamic Dashboard (Only visible after upload) --- */}
      {hasUploaded && summary && (
        <>
          {/* Detailed Summary Card */}
          <div className="card summary-card">
            <h2>Detailed Summary</h2>
            <div className="summary-grid">
              <div className="summary-item">
                <h3>Total Equipment</h3>
                <p>{summary.total_equipment}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Flowrate</h3>
                <p>{summary.averages?.avg_flowrate}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Pressure</h3>
                <p>{summary.averages?.avg_pressure}</p>
              </div>
              <div className="summary-item">
                <h3>Avg Temperature</h3>
                <p>{summary.averages?.avg_temperature}</p>
              </div>
            </div>
          </div>
<div className="card">
  <h2>Equipment Distribution by Type</h2>
  
  <div style={{ height: "500px", position: "relative" }}> 
    <Bar
      data={{
        labels: summary.type_distribution.map((i) => i.equipment_type),
        datasets: [
          {
            label: "Equipment Count",
            data: summary.type_distribution.map((i) => i.count),
            backgroundColor: "#4f46e5",
            borderRadius: 6,
            barPercentage: 0.8,      
            categoryPercentage: 0.9, 
          },
        ],
      }}
      options={{
        responsive: true,
        maintainAspectRatio: false, 
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
             
              font: { size: 14 }
            }
          },
          x: {
            ticks: {
              
              font: { size: 14 }
            }
          }
        },
        plugins: {
          legend: {
            labels: { font: { size: 14 } }
          }
        }
      }}
    />
  </div>
</div>

          {/* Report Export Action */}
          <div className="card center">
            <button className="pdf-btn" onClick={generatePDF}>
              📄 Generate Professional PDF Report
            </button>
          </div>

          {/* Raw Data Table */}
          <div className="card">
            <h2>Detailed Equipment List</h2>
            <div className="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Flowrate</th>
                    <th>Pressure</th>
                    <th>Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {equipments.map((eq) => (
                    <tr key={eq.id}>
                      <td>{eq.name}</td>
                      <td>{eq.equipment_type}</td>
                      <td>{eq.flowrate}</td>
                      <td>{eq.pressure}</td>
                      <td>{eq.temperature}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
