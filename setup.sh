mkdir -p ~/.streamlit/

echo "\
[server]\n\
port=$PORT\n\
enablleCORS=false\n\
headless=true\n\
\n\
" > ~/.streamlit/config.toml