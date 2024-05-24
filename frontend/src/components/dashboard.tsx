import React, { FormEvent, useEffect, useState } from "react";
import CSRFToken from "./CSRFToken";
import axios from "axios";
import Cookies from "js-cookie";
import {
  AppBar,
  Toolbar,
  Typography,
  TextField,
  Button,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Container,
  CssBaseline,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { styled } from "@mui/system";

const RootContainer = styled(Container)({
  marginTop: "20px",
});

const AppBarStyled = styled(AppBar)({
  marginBottom: "20px",
});

const LogoutButton = styled(Button)({
  marginLeft: "auto",
});


interface Stock {
  symbol: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
}


interface User {
  username: string;
}

const Dashboard: React.FC = () => {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [symbol, setSymbol] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    fetchStocks();
    fetchUser();
  }, []);


  const fetchStocks = async () => {
    try {
      const response = await axios.get("/api/user_stocks/");
      if (Array.isArray(response.data)) {
        setStocks(response.data);
      } else {
        setStocks([]);
        console.error("Expected array but got:", response.data);
      }
    } catch (error) {
      console.error("Error fetching stocks:", error);
      setStocks([]);
    }
  };

  const fetchUser = async () => {
    try {
      const response = await axios.get("/api/user/");
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  };

  const handleAddStock = async (e: FormEvent) => {
    e.preventDefault();
    const config = {
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
      }
    };

    const body = JSON.stringify({ symbol });
    try {
      const response = await axios.post("/api/user_stocks/",body, config);
      setMessage(response.data.message);
      console.log(message);
      setSymbol("");
      fetchStocks();
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setMessage(error.response?.data?.message || "An error occurred");
        console.error("Error adding stock:", error);
      } else {
        setMessage("An unexpected error occurred");
        console.error("Unexpected error:", error);
      }
    }
  };



  const handleDeleteStock = async (stockSymbol: string) => {
    try {
      await axios.delete("/api/user_stocks/", {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        data: {
          symbol: JSON.stringify({ symbol: stockSymbol }),
        },
      });
      fetchStocks();
    } catch (error) {
      console.error("Error deleting stock:", error);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post("/api/logout/");
      window.location.href = "/login"; // Redirect to login page after logout
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <RootContainer>
      <CssBaseline />
      <AppBarStyled position="static">
        <Toolbar>
          <Typography variant="h6">
            {user ? `Hi, ${user.username}` : "Loading..."}
          </Typography>
          <LogoutButton color="inherit" onClick={handleLogout}>
            Logout
          </LogoutButton>
        </Toolbar>
      </AppBarStyled>
      <form onSubmit={handleAddStock}>
        <CSRFToken/>
        <TextField
          label="Add Stock"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          fullWidth
        />
        {message && <p>{message}</p>}
        <Button
          variant="contained"
          color="primary"
          type="submit"
          style={{ marginTop: "10px" }}
        >
          Add Stock
        </Button>
      </form>
      <List>
        {stocks.map((stock: Stock) => (
          <ListItem key={stock.symbol}>
            <ListItemText
              primary={stock.symbol}
              secondary={`O: ${stock.open} H: ${stock.high} L: ${stock.low} C: ${stock.close} V: ${stock.volume}`}
            />
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleDeleteStock(stock.symbol)}
              >
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </RootContainer>
  );
};

export default Dashboard;
