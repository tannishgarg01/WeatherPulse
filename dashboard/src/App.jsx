
import { useEffect, useState } from "react";

import {
  LayoutDashboard,
  CloudSun,
  MapPin,
  Droplets,
  Wind,
  Thermometer,
  Menu,
  RefreshCw,
  Activity,
  Table2
} from "lucide-react";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [kpis, setKpis] = useState(null);
  const [cities, setCities] = useState([]);
  const [daily, setDaily] = useState([]);
  const [hourly, setHourly] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch all dashboard data
  async function fetchDashboardData() {
    try {
      setLoading(true);
      setError("");

      const [
        kpiRes,
        cityRes,
        dailyRes,
        hourlyRes
      ] = await Promise.all([
        fetch(`${API_URL}/api/weather/kpis`),
        fetch(`${API_URL}/api/weather/summary`),
        fetch(`${API_URL}/api/weather/daily`),
        fetch(`${API_URL}/api/weather/hourly`)
      ]);

      if (
        !kpiRes.ok ||
        !cityRes.ok ||
        !dailyRes.ok ||
        !hourlyRes.ok
      ) {
        throw new Error("Unable to fetch dashboard data");
      }

      const [
        kpiData,
        cityData,
        dailyData,
        hourlyData
      ] = await Promise.all([
        kpiRes.json(),
        cityRes.json(),
        dailyRes.json(),
        hourlyRes.json()
      ]);

      setKpis(kpiData);
      setCities(cityData);
      setDaily(dailyData);
      setHourly(hourlyData);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // KPI cards
  const stats = [
    {
      title: "Average Temperature",
      value: kpis ? `${kpis.average_temperature}°C` : "--",
      subtitle: "Across 7 cities",
      icon: Thermometer,
      style: "blue"
    },
    {
      title: "Average Humidity",
      value: kpis ? `${kpis.average_humidity}%` : "--",
      subtitle: "Relative humidity",
      icon: Droplets,
      style: "cyan"
    },
    {
      title: "Total Precipitation",
      value: kpis ? `${kpis.total_precipitation} mm` : "--",
      subtitle: "7-day forecast",
      icon: CloudSun,
      style: "purple"
    },
    {
      title: "Maximum Wind Speed",
      value: kpis ? `${kpis.maximum_wind_speed} km/h` : "--",
      subtitle: "Highest recorded",
      icon: Wind,
      style: "orange"
    }
  ];

  // Chart data preparation
  const dailyChartData = daily.map(item => ({
    ...item,
    date: item.full_date.slice(5)
  }));

  const hourlyChartData = hourly.map(item => ({
    ...item,
    time: `${String(item.hour).padStart(2, "0")}:00`
  }));

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <h2 className="logo">☁ WeatherPulse</h2>

        <p className="menu-title">MENU</p>

        <div className="nav-item active">
          <LayoutDashboard size={19} />
          Overview
        </div>

        <div className="nav-item">
          <CloudSun size={19} />
          Weather Analytics
        </div>

        <div className="nav-item">
          <MapPin size={19} />
          Cities
        </div>

        <div className="sidebar-bottom">
          <p>DATA ENGINEERING PROJECT</p>
          <span>WeatherPulse v1.0</span>
        </div>

      </aside>

      {/* Main Dashboard */}
      <main className="main">

        {/* Header */}
        <header className="topbar">

          <div className="heading">
            <Menu size={22} className="mobile-menu" />

            <div>
              <h1>Weather Dashboard</h1>
              <p>
                Monitor weather conditions across Indian cities
              </p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            API Connected
          </div>

        </header>

        {/* Welcome */}
        <section className="welcome">

          <div>
            <h2>Weather Overview</h2>
            <p>Your weather intelligence at a glance.</p>
          </div>

          <button
            onClick={fetchDashboardData}
            className="refresh-button"
            disabled={loading}
          >
            <RefreshCw size={16} />
            {loading ? "Loading..." : "Refresh Data"}
          </button>

        </section>

        {error && (
          <div className="error-message">
            {error}. Please check whether FastAPI is running.
          </div>
        )}

        {/* KPI Cards */}
        <section className="stats-grid">

          {stats.map(stat => {
            const Icon = stat.icon;

            return (
              <div className="stat-card" key={stat.title}>

                <div className={`stat-icon ${stat.style}`}>
                  <Icon />
                </div>

                <p>{stat.title}</p>

                <h2>
                  {loading ? "Loading..." : stat.value}
                </h2>

                <span>{stat.subtitle}</span>

              </div>
            );
          })}

        </section>

        {/* Daily Temperature and Rainfall */}
        <section className="content-grid">

          <div className="panel">

            <h3>Temperature Trends</h3>
            <p>Daily average temperature across cities</p>

            <div className="chart-container">

              {dailyChartData.length > 0 && (
                <ResponsiveContainer width="100%" height="100%">

                  <LineChart data={dailyChartData}>

                    <CartesianGrid
                      stroke="#293951"
                      strokeDasharray="3 3"
                    />

                    <XAxis dataKey="date" stroke="#91a2ba" />
                    <YAxis stroke="#91a2ba" unit="°C" />

                    <Tooltip
                      contentStyle={{
                        background: "#111a2d",
                        border: "1px solid #34445f",
                        borderRadius: "8px",
                        color: "#fff"
                      }}
                    />

                    <Line
                      type="monotone"
                      dataKey="avg_temperature"
                      name="Average Temperature"
                      stroke="#60a5fa"
                      strokeWidth={3}
                      dot={{ r: 4, fill: "#60a5fa" }}
                      activeDot={{ r: 7 }}
                    />

                  </LineChart>

                </ResponsiveContainer>
              )}

            </div>
          </div>

          <div className="panel">

            <h3>Rainfall Overview</h3>
            <p>Precipitation comparison by city</p>

            <div className="chart-container">

              {cities.length > 0 && (
                <ResponsiveContainer width="100%" height="100%">

                  <BarChart
                    data={cities}
                    margin={{
                      top: 10,
                      right: 5,
                      left: -15,
                      bottom: 5
                    }}
                  >

                    <CartesianGrid
                      stroke="#293951"
                      strokeDasharray="3 3"
                    />

                    <XAxis
                      dataKey="city_name"
                      stroke="#91a2ba"
                      tick={{ fontSize: 10 }}
                      interval={0}
                      angle={-25}
                      textAnchor="end"
                      height={55}
                    />

                    <YAxis stroke="#91a2ba" />

                    <Tooltip
                      contentStyle={{
                        background: "#111a2d",
                        border: "1px solid #34445f",
                        borderRadius: "8px",
                        color: "#fff"
                      }}
                    />

                    <Bar
                      dataKey="total_precipitation"
                      name="Rainfall (mm)"
                      fill="#22d3ee"
                      radius={[5, 5, 0, 0]}
                    />

                  </BarChart>

                </ResponsiveContainer>
              )}

            </div>
          </div>

        </section>

        {/* Hourly Temperature */}
        <section className="panel hourly-panel">

          <div className="panel-heading">
            <div>
              <h3>24-Hour Temperature Analysis</h3>
              <p>Average temperature across all monitored cities</p>
            </div>

            <span className="city-count">24 Hours</span>
          </div>

          <div className="chart-container">

            {hourlyChartData.length > 0 && (
              <ResponsiveContainer width="100%" height="100%">

                <LineChart data={hourlyChartData}>

                  <CartesianGrid
                    stroke="#293951"
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="time"
                    stroke="#91a2ba"
                    interval={2}
                  />

                  <YAxis stroke="#91a2ba" unit="°C" />

                  <Tooltip
                    contentStyle={{
                      background: "#111a2d",
                      border: "1px solid #34445f",
                      borderRadius: "8px",
                      color: "#fff"
                    }}
                  />

                  <Line
                    type="monotone"
                    dataKey="avg_temperature"
                    name="Average Temperature"
                    stroke="#a78bfa"
                    strokeWidth={3}
                    dot={false}
                    activeDot={{ r: 6 }}
                  />

                </LineChart>

              </ResponsiveContainer>
            )}

          </div>

        </section>

        {/* Monitored Cities */}
        <section className="panel cities-panel">

          <div className="panel-heading">

            <div>
              <h3>Monitored Cities</h3>
              <p>Live data from Gold Layer</p>
            </div>

            <span className="city-count">
              {cities.length} Cities
            </span>

          </div>

          <div className="city-list">

            {cities.map(city => (
              <div className="city-row" key={city.city_name}>

                <MapPin size={17} />

                <span>{city.city_name}</span>

                <strong>{city.avg_temperature}°C</strong>

                <span className="city-status">Monitoring</span>

              </div>
            ))}

          </div>

        </section>

        {/* Detailed Weather Table */}
        <section className="panel table-panel">

          <div className="panel-heading">

            <div>
              <h3>
                <Table2
                  size={19}
                  className="table-heading-icon"
                />
                Detailed City Weather
              </h3>

              <p>
                Weather statistics across all monitored cities
              </p>
            </div>

            <span className="city-count">
              {cities.length} Records
            </span>

          </div>

          <div className="table-wrapper">

            <table className="weather-table">

              <thead>
                <tr>
                  <th>City</th>
                  <th>Avg Temp</th>
                  <th>Min Temp</th>
                  <th>Max Temp</th>
                  <th>Humidity</th>
                  <th>Rainfall</th>
                  <th>Max Wind</th>
                </tr>
              </thead>

              <tbody>

                {cities.map(city => (

                  <tr key={city.city_name}>

                    <td className="table-city">
                      <MapPin size={15} />
                      {city.city_name}
                    </td>

                    <td>
                      {city.avg_temperature}°C
                    </td>

                    <td>
                      {city.min_temperature}°C
                    </td>

                    <td>
                      {city.max_temperature}°C
                    </td>

                    <td>
                      {city.avg_humidity}%
                    </td>

                    <td>
                      {city.total_precipitation} mm
                    </td>

                    <td>
                      {city.max_wind_speed} km/h
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

            {loading && (
              <p className="table-message">Loading city data...</p>
            )}

            {!loading && !error && cities.length === 0 && (
              <p className="table-message">No city data available.</p>
            )}

          </div>

        </section>

        {/* Footer */}
        <footer>
          <Activity size={14} />
          WeatherPulse · React · FastAPI · SQLite Gold Layer
        </footer>

      </main>

    </div>
  );
}

export default App;