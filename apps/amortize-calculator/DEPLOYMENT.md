# Vercel Deployment Guide

This guide walks you through deploying the Loan Amortization Calculator to Vercel.

## Quick Start (Connected Git - Recommended)

### 1. Ensure PR is Merged
The calculator code must be on the `main` branch. Make sure PR #2 is merged:
- Visit: https://github.com/mir-quadri/amortize-platform/pull/2
- Click "Merge pull request" once reviews are complete

### 2. Connect to Vercel

1. Go to https://vercel.com
2. Sign in with your GitHub account
3. Click "Add New..." → "Project"
4. Select the `mir-quadri/amortize-platform` repository
5. Configure as follows:

   **Framework Preset:** Next.js
   
   **Project Name:** `amortize-calculator` (or your preference)
   
   **Root Directory:** `apps/amortize-calculator/`
   
   **Build Command:** `npm run build`
   
   **Output Directory:** `.next`
   
   **Install Command:** `npm install`
   
6. Click "Deploy"

Vercel will automatically:
- Detect the Next.js framework
- Build the project
- Deploy to production at: `https://amortize-calculator.vercel.app`

### 3. Configure Custom Domain (Optional)

To use a custom domain like `amortize.example.com`:

1. In Vercel Dashboard, go to Project Settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Alternative: Vercel CLI Deployment

If you prefer command-line deployment:

```bash
# Navigate to the calculator directory
cd apps/amortize-calculator

# Install Vercel CLI globally (if not already installed)
npm install -g vercel

# Deploy
vercel

# Follow the interactive prompts:
# - Confirm project setup
# - Link to existing project or create new one
# - Set base directory (apps/amortize-calculator)
```

## Environment Variables (If Needed)

Currently, the calculator requires no environment variables—all calculations happen client-side.

If future versions need backend integration:

1. In Vercel Dashboard → Project Settings → Environment Variables
2. Add variables as needed
3. Redeploy for changes to take effect

## Monitoring Deployments

### View Deployment Status
1. Vercel Dashboard → Your Project
2. "Deployments" tab shows all builds
3. Click any deployment to see logs

### Continuous Deployment
With connected Git:
- Every push to `main` automatically deploys
- Preview deployments created for each PR
- Rollback to any previous deployment anytime

## Testing the Deployment

Once live, test at: `https://amortize-calculator.vercel.app/amortize` (or your custom domain + `/amortize`)

1. Enter a loan amount (e.g., $300,000)
2. Enter annual rate (e.g., 6%)
3. Enter loan term (e.g., 360 months)
4. Verify the calculated monthly payment and schedule display correctly

## Troubleshooting

### Build Fails
Check the build logs in Vercel Dashboard:
1. Go to "Deployments"
2. Click the failed deployment
3. Scroll to "Build Logs" for error details
4. Common issues: Node version mismatch, missing dependencies

### Environment
Vercel uses Node.js 18+. If you see version errors:
1. In Vercel Dashboard → Project Settings → Environment
2. Set Node.js version to 18 or higher

### Preview Deployments Not Working
Make sure the PR base branch is `main` and all CI checks pass before merging.

## Rollback to Previous Version

If deployment has issues:
1. Vercel Dashboard → Deployments
2. Click a previous successful deployment
3. Click the three dots menu → "Promote to Production"

## Additional Resources

- [Vercel Next.js Documentation](https://vercel.com/docs/frameworks/nextjs)
- [Calculator README](./README.md)
- [GitHub Repository](https://github.com/mir-quadri/amortize-platform)

## Support

For deployment issues, check:
- Vercel Dashboard error logs
- GitHub Actions CI logs
- Calculator README troubleshooting section
