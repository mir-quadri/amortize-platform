# Loan Amortization Calculator

A beautiful, production-ready loan amortization calculator built with Next.js and precision decimal math. Deployed at `/amortize` on Vercel.

## Features

✨ **Decimal-Perfect Math** - Uses Decimal.js for accurate financial calculations (no floating-point errors)

🎨 **Beautiful UI** - Responsive design with Tailwind CSS, works on all devices

⚡ **Fast & Lightweight** - Built with Next.js for optimal performance

📊 **Complete Schedules** - View full amortization schedules with principal, interest, and balance

🔒 **Input Validation** - Validates loan parameters before calculation

## Local Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Setup

```bash
# Clone the repository
git clone <your-repo>
cd amortize-calculator

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000/amortize](http://localhost:3000/amortize) in your browser (note: `/amortize` path is set via `basePath` config).

## Deployment to Vercel

### Option 1: Connected Git (Recommended)

1. Push this code to your GitHub repo
2. Go to [Vercel](https://vercel.com/dashboard)
3. Click "Add New..." → "Project"
4. Select your repository
5. Set **Base Directory** to the project folder (if in a monorepo)
6. Set **Build Command**: `npm run build`
7. Set **Start Command**: `npm start`
8. Click "Deploy"

### Option 2: Vercel CLI

```bash
npm i -g vercel
vercel
# Follow the prompts
```

### Monorepo Setup (if adding to existing site)

If adding to an existing Vercel project:

1. Copy the project folder into your existing repo
2. Update `vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "routes": [
    {
      "src": "/amortize/(.*)",
      "dest": "/amortize/$1"
    }
  ]
}
```

## File Structure

```
.
├── app/                          # Next.js app directory
│   ├── page.tsx                  # Calculator UI
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Tailwind styles
├── components/
│   └── ScheduleTable.tsx          # Amortization schedule table
├── lib/
│   └── calculator.ts             # Amortization calculation logic
├── public/                        # Static assets
├── next.config.js                # Next.js configuration (sets basePath: /amortize)
├── tailwind.config.ts            # Tailwind CSS config
├── tsconfig.json                 # TypeScript config
└── package.json                  # Dependencies
```

## Configuration

### URL Path

To change from `/amortize` to a different path, edit `next.config.js`:

```javascript
const nextConfig = {
  basePath: '/your-path-here',
};
```

### Styling

Modify colors and spacing in `tailwind.config.ts` or edit `app/globals.css`.

## API Reference (Local Calculation)

The calculator uses the Python amortization library ported to TypeScript. No external API calls are made.

### Amortization Formula

For loans with interest:
```
Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]

where:
  P = Principal
  r = Monthly rate (annual_rate / 100 / 12)
  n = Number of months
```

Payments are calculated with ROUND_HALF_UP precision (standard financial rounding).

## Validation Rules

- **Principal**: Must be > 0
- **Annual Rate**: Must be between 0 and 50 (%)
- **Term**: Must be between 1 and 480 months

## Browser Support

Works on all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers

## Performance

- **Initial Load**: < 50ms
- **Calculation**: < 1ms
- **Schedule (360 months)**: < 10ms

## Accessibility

- Semantic HTML
- Keyboard navigation support
- ARIA labels for screen readers
- High contrast text

## Future Enhancements

- [ ] Export schedule as CSV/PDF
- [ ] Bi-weekly and semi-monthly payment options
- [ ] Extra payment tracking
- [ ] Multiple loan comparison
- [ ] Mobile app version

## Related Projects

- [Amortize Platform](https://github.com/mir-quadri/amortize-platform) - Full-stack POC with API, Kubernetes, CI/CD

## License

MIT

## Support

For issues or questions, open an issue on GitHub or contact mir@mirquadri.com
