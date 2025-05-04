import { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import {
  Box,
  Container,
  Typography,
  InputBase,
  IconButton,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Card,
  CardMedia,
  CardContent,
  CircularProgress,
  CssBaseline,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const categories = ['Womenwear', 'Menswear', 'Couture'];
const seasons = ['Fall/Winter 2025', 'Spring/Summer 2025'];
const cities = ['Paris', 'Milan', 'New York', 'London'];

const theme = createTheme({
  typography: {
    fontFamily: `'Playfair Display', 'Helvetica Neue', serif`,
  },
  palette: {
    background: {
      default: '#f9f9f9',
    },
    text: {
      primary: '#1a1a1a',
      secondary: '#555',
    },
  },
});

export default function App() {
  const [query, setQuery] = useState('bohemian');
  const [category, setCategory] = useState('Womenwear');
  const [season, setSeason] = useState('Fall/Winter 2025');
  const [city, setCity] = useState('Paris');
  const [designer, setDesigner] = useState('All Designers');
  const [designers, setDesigners] = useState(['All Designers']);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);

  const observerRef = useRef(null);

  const search = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/search', {
        query,
        top_k: 24,
        page,
      });

      const imgs = response.data.results;

      setResults((prev) => {
        const combined = [...prev, ...imgs];
        const unique = Array.from(new Set(combined));
        return unique;
      });
      

      const foundDesigners = new Set(
        [...results, ...imgs].map((img) => {
          const parts = decodeURIComponent(img).split('/');
          return parts[parts.length - 2];
        })
      );
      setDesigners(['All Designers', ...Array.from(foundDesigners).sort()]);
    } catch (error) {
      console.error('Search failed:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    search();
    // eslint-disable-next-line
  }, [page]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setResults([]);
    setPage(1);
    search();
  };

  const filteredResults =
    designer === 'All Designers'
      ? results
      : results.filter((img) => {
          const parts = decodeURIComponent(img).split('/');
          return parts[parts.length - 2] === designer;
        });

  useEffect(() => {
    const el = document.getElementById('load-more-trigger');
    if (!el) return;

    if (observerRef.current) observerRef.current.disconnect();

    observerRef.current = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !loading) {
        setPage((prev) => prev + 1);
      }
    });

    observerRef.current.observe(el);

    return () => observerRef.current.disconnect();
  }, [results, loading]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 5 }}>
        <Typography
          variant="h3"
          gutterBottom
          fontWeight="bold"
          letterSpacing={1}
          textAlign="center"
        >
          RunwayIntel
        </Typography>
        <Typography
          variant="h6"
          color="text.secondary"
          textAlign="center"
          mb={4}
        >
          Explore the latest runway looks, styles, and designers
        </Typography>

        {/* Search Bar */}
        <Box display="flex" justifyContent="center" mb={3}>
        <Box
              component="form"
              onSubmit={handleSearchSubmit}
              sx={{
                height: 38,
                display: 'flex',
                alignItems: 'center',
                width: 360,
                boxShadow: 1,
                borderRadius: '999px',
                backgroundColor: 'white',
                px: 1.5,
              }}
            >

              <InputBase
                sx={{
                  ml: 1,
                  flex: 1,
                  fontSize: '0.85rem',
                  py: 0.5,
                }}

              placeholder="Search (e.g. 'leather jacket')"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <IconButton type="submit" sx={{ p: '10px' }}>
              <SearchIcon />
            </IconButton>
          </Box>
        </Box>

        {/* Filters */}
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 2,
            justifyContent: 'center',
            mb: 4,
          }}
        >
          {[
            ['Category', category, setCategory, categories],
            ['Season', season, setSeason, seasons],
            ['City', city, setCity, cities],
            ['Designer', designer, setDesigner, designers],
          ].map(([label, value, setter, options]) => (
            <FormControl
                  key={label}
                  sx={{
                    minWidth: 160,
                    '& .MuiInputBase-root': {
                      borderRadius: '999px',
                      border: '1px solid #ccc',
                      padding: '0px 10px',
                      backgroundColor: '#fff',
                      height: 36,
                      fontSize: '0.85rem',
                    },
                    '& .MuiInputLabel-root': {
                      fontSize: '0.75rem',
                      top: '-6px',
                    },
                    '& .MuiOutlinedInput-notchedOutline': {
                      border: 'none',
                    },
                    '& .MuiSelect-select': {
                      paddingTop: '4px',
                      paddingBottom: '4px',
                    },
                  }}
                >

              <InputLabel>{label}</InputLabel>
              <Select
                value={value}
                onChange={(e) => setter(e.target.value)}
                label={label}
                displayEmpty
              >
                {options.map((opt) => (
                  <MenuItem key={opt} value={opt}>
                    {opt}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          ))}
        </Box>

        {/* Results Grid */}
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
            gap: 3,
          }}
        >
          {filteredResults.map((img, i) => {
            const parts = decodeURIComponent(img).split('/');
            const filename = parts.pop();
            const designer = parts.pop();

            const rawName = filename
              .replace(/\.[^.]+$/, '')
              .replace(/[-_]/g, ' ');
            let subtitle = rawName
              .replace(new RegExp(`^${designer}\\s*`, 'i'), '')
              .trim();

            let tokens = subtitle
              .split(' ')
              .filter(
                (t) =>
                  ![
                    'fashion',
                    'week',
                    'paris',
                    'chloe',
                    'hermes',
                    'courreges',
                    'alaia',
                    'alexander',
                    'mcqueen',
                  ].includes(t.toLowerCase())
              );
            let lookNum = tokens.pop();
            subtitle = `${tokens.join(' ')} - Look ${lookNum}`;

            return (
              <Card
                key={i}
                sx={{
                  borderRadius: 4,
                  overflow: 'hidden',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                  transition: 'transform 0.25s ease, box-shadow 0.25s ease',
                  backgroundColor: '#fff',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
                  },
                }}
              >

                <CardMedia
                  component="img"
                  height="300"
                  image={img}
                  alt={filename}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ px: 2, py: 1 }}>
                  <Typography
                    variant="body2"
                    fontWeight="bold"
                    letterSpacing={1}
                  >
                    {designer.toUpperCase()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {subtitle}
                  </Typography>
                </CardContent>
              </Card>
            );
          })}
        </Box>

        {/* Infinite Scroll Trigger */}
        <Box id="load-more-trigger" height={20} />

        {/* Loading Spinner */}
        {loading && (
          <Box display="flex" justifyContent="center" py={5}>
            <CircularProgress />
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}
