# Optimal meeting point model

Given a triangle $△ABC$, we want to find a point $M$ such that:

$$min(f) = min(\frac{\overline{AM}+\overline{BM}+2\overline{MC}}{\overline{MC}})$$

That this is equivalent to:

$$min(f) = min(\frac{\overline{AM}+\overline{BM}}{\overline{MC}})$$

Subject to the following constraints:

$$C_1: \frac{\overline{AM}+\overline{MC}}{\overline{AC}} = \frac{\overline{BM}+\overline{MC}}{\overline{BC}}$$

$$C_2: M \in △ABC$$

## Real world application

This model is inspired by the following real world problem:

- Two friends Alice ($A$) and Bob ($B$) want to meet to go to the cinema ($C$).
- They want to maximize the covered distance together ($\overline{MC}$).
- They want to minimize the sum of the distance they cover individually ($\overline{AM}+\overline{MC}$ for Alice and $\overline{BM}+\overline{MC}$).
- They want their respective detours being percentually equal ($\frac{\overline{AM}+\overline{MC}}{\overline{AC}} = \frac{\overline{BM}+\overline{MC}}{\overline{BC}}$). We call this condition $\textit{fairness}$.

In order to find a compromise between the two objectives, we define $f$ as the ratio above.

## Example of the usage

In the figure below, we present an example of the usage of the proposed model. As a comparison, $G$ is the barycenter of the triangle. We observe that, while the value of $f$ is smaller in the case of $G$ with respect to the case of $M$, the $\textit{fairness}$ constraint involving the detours is not satisfied ($dA \neq dB$).

![meetingPoint](https://github.com/user-attachments/assets/c59dccf7-974e-49c3-9a30-8d4c3106a9fa)

