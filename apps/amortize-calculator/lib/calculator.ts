import Decimal from 'decimal.js';

export interface AmortizationScheduleEntry {
  month: number;
  payment: string;
  principal: string;
  interest: string;
  balance: string;
}

export interface AmortizationResult {
  monthly_payment: string;
  total_interest: string;
  schedule: AmortizationScheduleEntry[];
}

export function calculateMonthlyPayment(
  principal: Decimal,
  annualRatePct: Decimal,
  termMonths: number
): Decimal {
  if (principal.lte(0)) throw new Error('principal must be > 0');
  if (annualRatePct.lt(0) || annualRatePct.gt(50)) {
    throw new Error('annual_rate_pct must be between 0 and 50');
  }
  if (termMonths < 1 || termMonths > 480) {
    throw new Error('term_months must be between 1 and 480');
  }

  if (annualRatePct.eq(0)) {
    return principal.div(termMonths).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
  }

  const monthlyRate = annualRatePct.div(100).div(12);
  const onePlusRate = new Decimal(1).plus(monthlyRate);
  const numerator = principal.times(monthlyRate).times(onePlusRate.pow(termMonths));
  const denominator = onePlusRate.pow(termMonths).minus(1);

  return numerator.div(denominator).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

export function calculateAmortization(
  principal: Decimal,
  annualRatePct: Decimal,
  termMonths: number
): AmortizationResult {
  const monthlyPayment = calculateMonthlyPayment(principal, annualRatePct, termMonths);
  const monthlyRate = annualRatePct.gt(0)
    ? annualRatePct.div(100).div(12)
    : new Decimal(0);

  const schedule: AmortizationScheduleEntry[] = [];
  let balance = new Decimal(principal);
  let totalInterest = new Decimal(0);

  for (let month = 1; month <= termMonths; month++) {
    const interestPayment = balance
      .times(monthlyRate)
      .toDecimalPlaces(2, Decimal.ROUND_HALF_UP);

    let principalPayment: Decimal;
    let payment: Decimal;

    if (month === termMonths) {
      principalPayment = balance;
      payment = principalPayment.plus(interestPayment);
    } else {
      principalPayment = monthlyPayment
        .minus(interestPayment)
        .toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
      principalPayment = Decimal.min(principalPayment, balance);
      payment = principalPayment.plus(interestPayment);
    }

    balance = balance.minus(principalPayment).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
    totalInterest = totalInterest.plus(interestPayment).toDecimalPlaces(2, Decimal.ROUND_HALF_UP);

    schedule.push({
      month,
      payment: payment.toFixed(2),
      principal: principalPayment.toFixed(2),
      interest: interestPayment.toFixed(2),
      balance: Decimal.max(balance, 0).toFixed(2),
    });
  }

  return {
    monthly_payment: monthlyPayment.toFixed(2),
    total_interest: totalInterest.toFixed(2),
    schedule,
  };
}
