import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CSRFToken: React.FC = () => {
    const [csrftoken, setcsrftoken] = useState<string>('');

    const getCookie = (name: string): string | null => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get("/api/csrf_cookie/");
                console.log(res);
            } catch (err) {
                console.error('Error fetching CSRF token:', err);
            }
        };

        fetchData();
        setcsrftoken(getCookie('csrftoken') || '');
    }, []);

    return (
        <input type='hidden' name='csrfmiddlewaretoken' value={csrftoken} />
    );
};

export default CSRFToken;
