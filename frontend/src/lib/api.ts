import { env } from '$env/dynamic/public';

const API_BASE = env.PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

export interface PropertyListItem {
  id: number;
  title: string;
  price: string;
  listing_type: string;
  property_type: string | null;
  bedrooms: number;
  bathrooms: number;
  area_sqm: string | null;
  lot_sqm?: string | null;
  parking_spaces?: number;
  year_built?: number | null;
  condition?: string | null;
  pet_friendly?: boolean;
  furnished?: boolean;
  city: string;
  region: string;
  thumbnail_url: string | null;
}

export interface PropertyDetail extends PropertyListItem {
  description: string;
  address: string;
  country: string;
  lot_sqm?: string | null;
  parking_spaces?: number;
  year_built?: number | null;
  condition?: string | null;
  pet_friendly?: boolean;
  furnished?: boolean;
  features: string[];
  images: { id: number; image: string; caption: string; order: number }[];
  created_at: string;
}

export interface PropertiesResponse {
  items: PropertyListItem[];
  count: number;
}

export interface FilterOption {
  id: number;
  name: string;
  slug: string;
}

export interface FiltersResponse {
  property_types: FilterOption[];
  features: FilterOption[];
  cities: string[];
  regions: string[];
  conditions: { value: string; label: string }[];
  price_min: number | null;
  price_max: number | null;
  area_min: number | null;
  area_max: number | null;
  lot_min: number | null;
  lot_max: number | null;
  year_min: number | null;
  year_max: number | null;
}

export interface PropertyFilters {
  search?: string;
  listing_type?: string;
  property_type?: string;
  min_price?: number;
  max_price?: number;
  bedrooms?: number;
  bathrooms?: number;
  min_area?: number;
  max_area?: number;
  min_lot?: number;
  max_lot?: number;
  min_year?: number;
  max_year?: number;
  parking?: number;
  condition?: string;
  pet_friendly?: boolean;
  furnished?: boolean;
  listed_since?: number;
  city?: string;
  region?: string;
  features?: string[];
  sort?: string;
  page?: number;
}

function buildQuery(params: PropertyFilters): string {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v === undefined || v === null) return;
  if (v === '' && k !== 'search') return;
    if (k === 'features' && Array.isArray(v)) {
      if (v.length) search.set('features', v.join(','));
    } else if (k === 'search') {
      if (typeof v === 'string' && v.trim()) search.set('search', v.trim());
    } else {
      search.set(k, String(v));
    }
  });
  const q = search.toString();
  return q ? `?${q}` : '';
}

export async function fetchProperties(filters: PropertyFilters = {}): Promise<PropertiesResponse> {
  const res = await fetch(`${API_BASE}/properties${buildQuery(filters)}`);
  if (!res.ok) throw new Error('Failed to fetch properties');
  return res.json();
}

export async function fetchProperty(id: number): Promise<PropertyDetail> {
  const res = await fetch(`${API_BASE}/properties/${id}`);
  if (!res.ok) throw new Error('Property not found');
  return res.json();
}

export async function fetchFilters(): Promise<FiltersResponse> {
  const res = await fetch(`${API_BASE}/filters`);
  if (!res.ok) throw new Error('Failed to fetch filters');
  return res.json();
}

export interface InquiryPayload {
  name: string;
  email: string;
  phone?: string;
  message: string;
}

export async function submitInquiry(propertyId: number, payload: InquiryPayload): Promise<{ success: boolean }> {
  const res = await fetch(`${API_BASE}/properties/${propertyId}/inquiry`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || err.message || 'Failed to submit inquiry');
  }
  return res.json();
}

export function getBaseUrl(): string {
  return env.PUBLIC_API_URL?.replace(/\/api\/?$/, '') || 'http://127.0.0.1:8000';
}

export function getImageUrl(path: string | null): string {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  return `${getBaseUrl()}${path}`;
}
